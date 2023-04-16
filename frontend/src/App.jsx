import { ChakraProvider } from "@chakra-ui/react";
import { useState } from "react";
import LoginForm from "./screens/LoginForm";
import Canvas from "./screens/Canvas";
import theme from "./theme";

function App() {
  const [isLoggedIn, toggleLoggedIn] = useState(true);

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
