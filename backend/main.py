import threading
import optparse
import grpc
import sys
import concurrent.futures
import time
import random
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

# dict for community delays
community_delays = {}

# lock for delays dictionaries
delay_lock = threading.Lock()
# lock for queue
queue_lock = threading.Lock()

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

def PPServicer(main_pb2_grpc.PPServicer):
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
        
        # community exists
        else if community in community_delays.keys():
            user_communities[username] = community
            message = "Successfully joined " + community

        # community doesn't exist
        else:
            community_delays[community] = default_community_delay
            user_communities[username] = community
            message = "Created and joined new community: " + community
        delay_lock.release()

        return main_pb2.UserResponse(message=message)


    def CheckActionDelay(self, request, context):
        '''
        Checks a user's action delay
        '''
        username = request.username
        
        delay_lock.acquire()
        if username not in user_delays.keys():
            message = "Error: User doesn't exist."
        else:
            delay = user_delays[username]
            message = "Delay for " + username + " is " + str(delay)
        delay_lock.release()

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
        
        '''
        username = request.username
        act = Action(request.color, request.row, request.col)

        delay_lock.acquire()
        if username not in user_delays.keys():
            delay_lock.release()
            return main_pb2.UserResponse(message="Error: User doesn't exist.")
        
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

        '''
        # TODO: needs more functionality

    def JoinCommunityTransaction(self, request, context):
        '''

        '''
        # TODO: needs more functionality

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

    while True:
        delay_lock.acquire()

        for user in user_delays.keys():
            val = user_delays[user]
            user_delays[user] = val - 1 if val > 0 else 0

        for community in community_delays.keys():
            val = user_delays[community]
            community_delays[community] = val - 1 if val > 0 else 0

        delay_lock.release()

        time.sleep(1.0 - ((time.time() - starttime) % 1.0))

def update_canvas():
    '''
    wakes up every 0.25 seconds and adds a pixel action to the canvas
    '''
    while True:
        time.sleep(0.1)
        queue_lock.acquire()

        if(len(action_queue) > 0):
            act = action_queue.pop(0)
            canvas[act.row][act.col] = act.color

        queue_lock.release()


def gracefully_shutdown():
    """
    Gracefully shuts down the server.
    @Parameter: None.
    @Returns: None.
    """
    print("Shutting down.") # UI message
    run_event.clear()
    server.stop(0)
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
        # TODO: start the two threads decrement_delays, update_canvas here
        # TODO: there needs to be a different thread that adds community transaction when it hits zero (needs data structure per community for actions list) {community: [Actions]}
        # TODO: something needs to handle delayed actions - maybe another structure holds delayed actions and a thread decrements then adds them to action queue? [(Action, delay)]

        server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
        main_pb2_grpc.add_PPServicer_to_server(PPServicer(), server)        

        global aws
        server_address = "{}:{}".format("0.0.0.0" if aws else "127.0.0.1", "3000")
        server.add_insecure_port(server_address)
        print("Started server on", server_address)
        server.start()
        server.wait_for_termination()
    
    except KeyboardInterrupt:
        gracefully_shutdown()
        
    return

if __name__ == '__main__':
    main()