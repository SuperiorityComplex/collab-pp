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
delay_lock = None
# lock for queue
queue_lock = None

canvas_dim = 10
canvas = []

def PPServicer(main_pb2_grpc.PPServicer):
    # TODO: fill in the backend
    def CreateUser(self, request, context):
        

    def JoinCommunity(self, request, context):
        

    def CheckActionDelay(self, request, context):
        

    def CheckCommunity(self, request, context):
        

    def NormalAction(self, request, context):
        

    def DelayedAction(self, request, context):
        

    def JoinCommunityTransaction(self, request, context):
        

    def DisplayCanvas(self, request, context):
        

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
    serialized = ','.join(str(pixel) for row in canvas for pixel in row)
    return serialized


def decrement_delays():
    # TODO: wake up every second, delay_lock, and decrement user_delays, community_delays

def update_canvas():
    # TODO: wake up every 0.1 second, queue_lock, update the canvas with one action

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