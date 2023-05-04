# collab-pp

Collaborative Pixel Painting (Basically Reddit Place)

# Running the front-end

1. Ensure that you have [Docker](https://docs.docker.com/get-docker/) installed
2. Run `frontend/src/generate_grpc.sh` to generate the gRPC code for the frontend
   - This is based off of the `main.proto` file in backend
3. Run `frontend/grpc_start.sh` to build the docker files for the grpc middleman.
   - If it gives you an error about an existing Docker build, you need to run:
     1. docker stop grpc-web-react
     2. docker run -d --name grpc-web-react -p 8080:8080 -p 9901:9901 grpc-web-react
   - Docker builds based off the specifications in `Dockerfile`. `Dockerfile` uses `envoy.yaml` to configure the envoy proxy. The envoy proxy is used to pass messages from the React frontend to the python gRPC backend.
4. Run `yarn install; yarn start` from the `frontend/` folder.  Frontend will be running on port 3001.
5. Start backend.

# Backend

Simply use `python main.py` from the `backend/` directory.

# Test scripts

Testing code using a Python gRPC client is available in `test_scripts/`

`action_simulator.py` can be used to simulate many distributed users and validate well-ordered actions. It can be used to stress test the system, and also vary the timing of action delays.

`blue_corner.py` tests the community batch function and verifies it is atomic.

`smiley_takeover.py` stress-tests the community function by showing that a community action can atomically cover the entire canvas.
