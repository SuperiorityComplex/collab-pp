import threading
import optparse
import grpc
import sys
import concurrent.futures
import time
import random
import copy
import json
sys.path.append('./grpc_stubs')
import main_pb2
import main_pb2_grpc

# Stores all the threads that are running. (Used for graceful shutdown)
running_threads = []

# Event that is set when threads are running and cleared when you want threads to stop
run_event = threading.Event()

# Set to True when deploying on aws
aws = False

# dict for users and their delays {username: delay}
user_delays = {}

# dict for users in a community {username: community}
user_communities = {}

# delayed actions [(delay, Action, username)]
delayed_actions = []
# delayed users [username]
delayed_users = []

# dict for community delays {community: delay}
community_delays = {}
# community batched actions {community: [Action]}
community_actions = {}
# users participating in community action {community: [username]}
community_transaction_users = {}

# lock for delays dictionaries
delay_lock = threading.Lock()
# lock for Action queue
queue_lock = threading.Lock()
# lock for delayed Actions
delayed_actions_lock = threading.Lock()
# lock for community transactions
community_transaction_lock = threading.Lock()

# queue of pixel actions
action_queue = []

canvas_dim = 10
canvas = []

default_community_delay = 120
default_user_delay = 60

class Action():
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col

class PPServicer(main_pb2_grpc.PPServicer):
    def CreateUser(self, request, context):
        '''
        Creates a user if it doesn't exist. If it does exist, fails.
        '''
        username = request.username
        
        delay_lock.acquire()
        if username in user_delays.keys():
            message = "Error: User already exists."
        else:
            user_delays[username] = 0
            user_communities[username] = "NO_COMM" # funny error possible if someone names their community this.
            message = "User successfully created."
        delay_lock.release()

        return main_pb2.UserResponse(message=message)

    def JoinCommunity(self, request, context):
        '''
        Joins a community.
        '''
        username = request.username
        community = request.community

        if community == "NO_COMM":
            return main_pb2.UserResponse(message="Invalid Community Name")

        delay_lock.acquire()
        if username not in user_communities.keys():
            message = "Error: User doesn't exist."

        # user is already part of a community
        if user_communities[username] != "NO_COMM":
            message = "Error: User is already part of community: " + user_communities[username]
        
        # community exists
        elif community in community_delays.keys():
            user_communities[username] = community
            message = "Successfully joined " + community

        # community doesn't exist
        else:
            community_transaction_lock.acquire()
            community_delays[community] = default_community_delay
            user_communities[username] = community
            community_actions[community] = []
            community_transaction_users[community] = []
            community_transaction_lock.release()

            message = "Created and joined new community: " + community

        delay_lock.release()

        return main_pb2.UserResponse(message=message)

    def CheckActionDelay(self, request, context):
        '''
        Checks a user's action delay
        '''
        username = request.username
        
        delay_lock.acquire()
        
        # user doesn't exist
        if username not in user_delays.keys():
            delay_lock.release()
            return main_pb2.UserResponse(message="Error: User doesn't exist.")
        
        # user has pending delayed action
        if username in delayed_users: # read-only, will not grab lock
            delay_lock.release()

            pending_delay = 0
            # honestly could be a concurrency issue but hope not lmao, only doing reads
            for delay, _, user in delayed_actions:
                if username == user:
                    pending_delay = delay
                    break

            message = username + " has a pending delayed action, which will be added in " + str(pending_delay)
            return main_pb2.UserResponse(message=message)
        
        # user is part of a community transaction
        community = user_communities[username]
        if community != "NO_COMM" and username in community_transaction_users[community]:
            comm_delay = community_delays[community]
            delay_lock.release()
            message = username + " is pending in a community transaction, which will be added in " + str(comm_delay)
            return main_pb2.UserResponse(message=message)

        else:
            delay = user_delays[username]
            delay_lock.release()
            message = "Delay for " + username + " is " + str(delay)
            return main_pb2.UserResponse(message=message)

    def CheckCommunity(self, request, context):
        '''
        Returns the name of the community that the user is in and its delay.
        '''
        username = request.username
        
        delay_lock.acquire()
        if username not in user_delays.keys():
            message = "Error: User doesn't exist."
        else:
            community = user_communities[username]
            if community == "NO_COMM":
                message = "You are not part of a community."
            else:
                delay = community_delays[community]
                message = "Delay for " + community + " is " + str(delay)
        delay_lock.release()

        return main_pb2.UserResponse(message=message)

    def NormalAction(self, request, context):
        '''
        Normal user action, no delay.
        '''
        username = request.username
        act = Action(request.color, request.row, request.col)

        delay_lock.acquire()
        
        # user doesn't exist
        if username not in user_delays.keys():
            delay_lock.release()
            return main_pb2.UserResponse(message="Error: User doesn't exist.")
        
        # user has pending delayed action
        if username in delayed_users: # read-only, will not grab lock
            delay_lock.release()

            pending_delay = 0
            # honestly could be a concurrency issue but hope not lmao, only doing reads
            for delay, _, user in delayed_actions:
                if username == user:
                    pending_delay = delay
                    break

            message = "Error: You have a pending delayed action, which will be added in " + str(pending_delay)
            return main_pb2.UserResponse(message=message)

        # user is already part of a community transaction
        community = user_communities[username]
        if community != "NO_COMM" and username in community_transaction_users[community]:
            delay_lock.release()
            return main_pb2.UserResponse(message="Error: User already in community transaction.")

        # user's delay is not yet done
        if user_delays[username] != 0:
            message = "Error: Cannot make an action, user delay is " + str(user_delays[username])
            delay_lock.release()
            return main_pb2.UserResponse(message=message)

        else:
            user_delays[username] = default_user_delay
            delay_lock.release()

            queue_lock.acquire()
            action_queue.append(act)
            queue_lock.release()

            message = "Successfully added action."

        return main_pb2.UserResponse(message=message)

    def DelayedAction(self, request, context):
        '''
        Add a delayed action for this user.
        '''
        username = request.username
        act = Action(request.color, request.row, request.col)
        delay = request.delay

        delay_lock.acquire()
        
        # user doesn't exist
        if username not in user_delays.keys():
            delay_lock.release()
            return main_pb2.UserResponse(message="Error: User doesn't exist.")
        
        # user has pending delayed action
        if username in delayed_users: # read-only, will not grab lock
            delay_lock.release()

            pending_delay = 0
            # honestly could be a concurrency issue but hope not lmao, only doing reads
            for delay, _, user in delayed_actions:
                if username == user:
                    pending_delay = delay
                    break

            message = "Error: You have a pending delayed action, which will be added in " + str(pending_delay)
            return main_pb2.UserResponse(message=message)

        # user is already part of a community transaction
        community = user_communities[username]
        if community != "NO_COMM" and username in community_transaction_users[community]:
            delay_lock.release()
            return main_pb2.UserResponse(message="Error: User already in community transaction.")

        # user's delay is not yet done
        if user_delays[username] > delay:
            message = "Error: Cannot make this delayed action, user delay is " + str(user_delays[username])
            delay_lock.release()
            return main_pb2.UserResponse(message=message)

        else:
            user_delays[username] = 0
            delay_lock.release()

            delayed_actions_lock.acquire()
            delayed_users.append(username)
            delayed_actions.append((delay, act, username))
            delayed_actions_lock.release()

            message = "Successfully added delayed action."

        return main_pb2.UserResponse(message=message)

    def JoinCommunityTransaction(self, request, context):
        '''
        User joins community transaction
        '''
        username = request.username
        act = Action(request.color, request.row, request.col)

        delay_lock.acquire()
        
        # user doesn't exist
        if username not in user_delays.keys():
            delay_lock.release()
            return main_pb2.UserResponse(message="Error: User doesn't exist.")
        
        # user isn't part of a community
        if user_communities[username] == "NO_COMM":
            delay_lock.release()
            return main_pb2.UserResponse(message="Error: User not part of a community.")

        # user has pending delayed action
        if username in delayed_users: # read-only, will not grab lock
            delay_lock.release()

            pending_delay = 0
            for delay, _, user in delayed_actions:
                if username == user:
                    pending_delay = delay
                    break

            message = "Error: You have a pending delayed action, which will be added in " + str(pending_delay)
            return main_pb2.UserResponse(message=message)

        community = user_communities[username]
        community_delay = community_delays[community]

        # user is already part of a community transaction
        if username in community_transaction_users[community]:
            delay_lock.release()
            return main_pb2.UserResponse(message="Error: User already in community transaction.")

        # user's delay is not yet done
        if user_delays[username] > community_delay:
            message = "Error: Cannot join community transaction, user delay is " + str(user_delays[username]) + " and community delay is " + str(community_delay)
            delay_lock.release()
            return main_pb2.UserResponse(message=message)

        else:
            user_delays[username] = 0
            delay_lock.release()

            community_transaction_lock.acquire()

            community_actions[community].append(act)
            community_transaction_users[community].append(username)
            
            community_transaction_lock.release()

            message = "Successfully joined community transaction."

        return main_pb2.UserResponse(message=message)

    def DisplayCanvas(self, request, context):
        '''
        Sends a serialized string of the canvas in csv format
        '''
        return main_pb2.Canvas(canvas = serialize_canvas())

def init_canvas():
    '''
    init canvas to empty
    '''
    global canvas
    canvas = [ ["#FFFFFF"]*canvas_dim for i in range(canvas_dim)]

def serialize_canvas():
    '''
    serialize the canvas to string to send over grpc
    '''
    global canvas

    queue_lock.acquire()
    serialized = ','.join(str(pixel) for row in canvas for pixel in row)
    queue_lock.release()

    return serialized

def decrement_delays():
    '''
    wake up every second and decrement user_delays, community_delays
    '''
    starttime = time.time()

    while run_event.is_set():
        delay_lock.acquire()

        for user in user_delays.keys():
            val = user_delays[user]
            user_delays[user] = val - 1 if val > 0 else 0

        for community in community_delays.keys():
            val = user_delays[community]
            community_delays[community] = val - 1 if val > 0 else 0

            if community_delays[community] == 0:
                community_transaction(community)

        delay_lock.release()

        time.sleep(1.0 - ((time.time() - starttime) % 1.0))

def community_transaction(community):
    '''
    process a community transaction since its delay has hit zero.
    should be holding delay_lock when this is called.
    '''
    # avoiding nested lock acquiring
    community_delays[community] = default_community_delay
    delay_lock.release()

    actions = []

    community_transaction_lock.acquire()

    if len(community_actions[community]) > 0:
        actions = copy.deepcopy(community_actions[community])
        community_actions[community] = []
        community_transaction_users[community] = []

    community_transaction_lock.release()

    queue_lock.acquire() 
    action_queue.extend(actions)
    queue_lock.release()

    delay_lock.acquire()

def update_canvas():
    '''
    wakes up every 0.1 seconds and adds a pixel action to the canvas
    '''
    global canvas

    while run_event.is_set():
        time.sleep(0.1)
        queue_lock.acquire()

        if(len(action_queue) > 0):
            act = action_queue.pop(0)
            canvas[act.row][act.col] = act.color

        queue_lock.release()

def decrement_delayed_actions():
    '''
    wake up every second and decrement delayed_actions list, add to action queue if hits zero
    '''
    starttime = time.time()

    global delayed_actions

    while run_event.is_set():
        delayed_actions_lock.acquire()

        for i, (delay, act, username) in enumerate(delayed_actions):
            delayed_actions[i] = (delay-1, act, username)
            if delay <= 0:
                # add action to the queue
                queue_lock.acquire()
                action_queue.append(act)
                queue_lock.release()

                # release username, reset delay
                delay_lock.acquire()
                user_delays[username] = default_user_delay
                delay_lock.release()
                delayed_users.remove(username)
                
        delayed_actions = [i for i in delayed_actions if i[0] > -1]

        delayed_actions_lock.release()

        time.sleep(1.0 - ((time.time() - starttime) % 1.0))

def gracefully_shutdown():
    """
    Gracefully shuts down the server.
    @Parameter: None.
    @Returns: None.
    """
    print("Shutting down.") # UI message
    run_event.clear()
    try:
        for thread in running_threads:
            thread.join()
    except (OSError):
        # This occurs when the socket is already closed.
        pass
    sys.exit(0)

def main():
    run_event.set()
    try:
        init_canvas()
        decrement_thread = threading.Thread(target=(decrement_delays), args=())
        update_thread = threading.Thread(target=(update_canvas), args=())
        decrement_delayed_actions_thread = threading.Thread(target=(decrement_delayed_actions), args=())

        decrement_thread.start()
        update_thread.start()
        decrement_delayed_actions_thread.start()

        running_threads.append(decrement_thread)
        running_threads.append(update_thread)
        running_threads.append(decrement_delayed_actions_thread)
        
        server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
        main_pb2_grpc.add_PPServicer_to_server(PPServicer(), server)        

        global aws
        server_address = "{}:{}".format("0.0.0.0" if aws else "127.0.0.1", "3000")
        server.add_insecure_port(server_address)
        print("Started server on", server_address)
        server.start()
        server.wait_for_termination()
    
    except KeyboardInterrupt:
        server.stop(0)
        gracefully_shutdown()
        
    return

if __name__ == '__main__':
    main()