import { useRef, useState } from "react";
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  Stack,
  Center,
  VStack,
  Heading,
} from "@chakra-ui/react";
import Layout from "../components/Layout";
import MessageBanner from "../components/MessageBanner";
import client from "../grpc_stubs/PPClient";
import { useUser } from "../context/UserContext";
import { UserRequest } from "../grpc_stubs/protos/main_grpc_web_pb";

function LoginForm() {
  const { setUsername } = useUser();
  const [formUsername, setFormUsername] = useState("");
  const [error, setError] = useState(null);
  const messageTimer = useRef(null);

  const setServerMsgWrapper = (msg) => {
    clearTimeout(messageTimer.current);
    setError(msg);
    messageTimer.current = setTimeout(() => {
      setError(null);
    }, 1000);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const userRequest = new UserRequest();
    userRequest.setUsername(formUsername);
    client.createUser(userRequest, {}, (err, response) => {
      const msg = response.getMessage();
      if (
        err
        //  || msg === "Error: User already exists."
      ) {
        setServerMsgWrapper(msg);
      } else {
        setUsername(formUsername);
      }
    });
  };

  return (
    <Layout>
      {error && <MessageBanner message={error} />}
      <Box
        bg="gray.800"
        minH="100vh"
        display="flex"
        alignItems="center"
        justifyContent="center"
      >
        <Center>
          <Box p={12} maxW="md" borderWidth="1px" borderRadius="lg" bg="white">
            <VStack spacing={6}>
              <Heading size="md">enter details to see canvas</Heading>
              <form onSubmit={handleSubmit}>
                <Stack spacing={3} w="100%">
                  <FormControl isRequired>
                    <FormLabel>username</FormLabel>
                    <Input
                      type="text"
                      placeholder="Enter your username"
                      value={formUsername}
                      onChange={(event) => setFormUsername(event.target.value)}
                    />
                  </FormControl>
                  <Button
                    type="submit"
                    colorScheme="primary"
                    size="lg"
                    w="100%"
                  >
                    Log in
                  </Button>
                </Stack>
              </form>
            </VStack>
          </Box>
        </Center>
      </Box>
    </Layout>
  );
}

export default LoginForm;
