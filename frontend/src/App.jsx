import { ChakraProvider } from "@chakra-ui/react";
import { useState } from "react";
import LoginForm from "./screens/LoginForm";
import Canvas from "./screens/Canvas";
import theme from "./theme";
import { UserContext } from "./context/UserContext";

function App() {
  const [username, setUsername] = useState(null);

  const signOut = () => {
    setUsername(null);
  };

  return (
    <ChakraProvider theme={theme}>
      <UserContext.Provider value={{ username, setUsername, signOut }}>
        {username ? <Canvas /> : <LoginForm />}
      </UserContext.Provider>
    </ChakraProvider>
  );
}

export default App;
