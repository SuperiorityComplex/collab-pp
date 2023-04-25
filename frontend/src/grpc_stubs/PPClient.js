import { PPClient } from "./protos/main_grpc_web_pb";

const client = new PPClient("http://localhost:8080", null, null);

export default client;
