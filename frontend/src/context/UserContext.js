import { createContext, useContext } from "react";

const UserContext = createContext({
  username: null,
  signOut: () => {},
  setUsername: () => {},
});

function useUser() {
  return useContext(UserContext);
}

export { UserContext, useUser };
