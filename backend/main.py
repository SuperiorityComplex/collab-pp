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


def PPServicer(main_pb2_grpc.PPServicer):
    # TODO

'''
TODO: server threads
- response thread, responds to user requests (main thread started by start_server)
    does normal responses to user actions
    queue an action / transaction

- wake up every second and decrement user delays, community delays
- add to canvas by consuming from action queue, every 0.1 seconds
'''

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