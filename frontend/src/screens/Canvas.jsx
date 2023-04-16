import { Box } from "@chakra-ui/react";
import ColorGrid from "../components/ColorGrid";
import Layout from "../components/Layout";

const Canvas = () => {
  return (
    <Layout>
      <Box w="100vw" h="100vh">
        <ColorGrid />
      </Box>
    </Layout>
  );
};

export default Canvas;
