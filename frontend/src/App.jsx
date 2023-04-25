import { ChakraProvider } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import LoginForm from "./screens/LoginForm";
import Canvas from "./screens/Canvas";
import theme from "./theme";
import { UserRequest } from "./grpc_stubs/protos/main_pb";
import { PPClient } from "./grpc_stubs/protos/main_grpc_web_pb";

const client = new PPClient("http://localhost:8080", null, null);

function App() {
  const [isLoggedIn, toggleLoggedIn] = useState(true);

  useEffect(() => {
    const userRequest = new UserRequest();
    userRequest.setUsername("test1");
    client.createUser(userRequest, {}, (err, response) => {
      if (err) return console.log(err);
      const msg = response.getMessage();
      console.log(msg);
    });
  }, []);

  return (
    <ChakraProvider theme={theme}>
      {isLoggedIn ? (
        <Canvas />
      ) : (
        <LoginForm onSubmit={() => toggleLoggedIn(true)} />
      )}
    </ChakraProvider>
  );
}

export default App;
