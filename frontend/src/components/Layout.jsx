import React from "react";
import { Box } from "@chakra-ui/react";

function Layout({ children, backButton }) {
  return (
    <Box>
      <header></header>
      <main>{children}</main>
      <footer></footer>
    </Box>
  );
}

export default Layout;
