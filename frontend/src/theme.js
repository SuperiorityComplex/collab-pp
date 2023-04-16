import { extendTheme } from "@chakra-ui/react";

const theme = extendTheme({
  colors: {
    primary: {
      50: "#f5f7fb",
      100: "#d7e1f0",
      200: "#b4c7e2",
      300: "#8aa8d2",
      400: "#7296c9",
      500: "#527ebd",
      600: "#446ba0",
      700: "#375581",
      800: "#2e486d",
      900: "#21344e",
    },
    accent: {
      50: "#fef5f8",
      100: "#fbd7e3",
      200: "#f7b2ca",
      300: "#e78aaa",
      400: "#ce7b98",
      500: "#ae6880",
      600: "#93586c",
      700: "#764657",
      800: "#633c49",
      900: "#482b35",
    },
  },
});

export default theme;
