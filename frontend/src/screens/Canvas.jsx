import {
  chakra,
  Box,
  Heading,
  VStack,
  FormControl,
  FormLabel,
  Select,
  Input,
  Button,
  Divider,
} from "@chakra-ui/react";
import { SketchPicker } from "react-color";
import ColorGrid from "../components/ColorGrid";
import Layout from "../components/Layout";

const Canvas = () => {
  return (
    <Layout>
      <Box
        w="100vw"
        h="100vh"
        display="inline-flex"
        p="5%"
        alignItems="center"
        justifyContent="space-between"
      >
        <VStack display="flex" flexDir="column" w="60%" alignItems="flex-start">
          <Heading w="full">
            Drawing as{" "}
            <chakra.span textDecor="underline" color="primary.500">
              Ivan
            </chakra.span>
          </Heading>
          <Box w="full" h="60vw">
            <ColorGrid />
          </Box>
        </VStack>
        <VStack display="flex" flexDir="column" w="30%" alignItems="flex-start">
          <FormControl>
            <FormLabel htmlFor="draw-dropdown">Draw</FormLabel>
            <Select id="draw-dropdown" placeholder="Select drawing tool">
              <option value="pen">Pen</option>
              <option value="brush">Brush</option>
              <option value="eraser">Eraser</option>
            </Select>
          </FormControl>

          <FormControl>
            <FormLabel htmlFor="color-picker">Color</FormLabel>
            <SketchPicker id="color-picker" />
          </FormControl>

          <FormControl>
            <FormLabel htmlFor="community-input">Community</FormLabel>
            <Input
              type="text"
              id="community-input"
              placeholder="Enter community name"
            />
          </FormControl>
          <VStack w="full">
            <Divider my="5" />
            <Button colorScheme="primary">Create Community</Button>
          </VStack>
        </VStack>
      </Box>
    </Layout>
  );
};

export default Canvas;
