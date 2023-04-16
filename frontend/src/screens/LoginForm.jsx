import { useState } from "react";
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

function LoginForm({ onSubmit }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    // perform login logic here
    onSubmit();
  };

  return (
    <Layout>
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
                      value={username}
                      onChange={(event) => setUsername(event.target.value)}
                    />
                  </FormControl>

                  <FormControl isRequired>
                    <FormLabel>password</FormLabel>
                    <Input
                      type="password"
                      placeholder="Enter your password"
                      value={password}
                      onChange={(event) => setPassword(event.target.value)}
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
