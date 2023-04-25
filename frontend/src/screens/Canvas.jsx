import {
  chakra,
  Box,
  Heading,
  VStack,
  FormControl,
  FormLabel,
  Input,
  Button,
  Divider,
  Switch,
  HStack,
  Text,
} from "@chakra-ui/react";
import { SketchPicker } from "react-color";
import ColorGrid from "../components/ColorGrid";
import Layout from "../components/Layout";
import { useUser } from "../context/UserContext";
import { useState } from "react";

const Canvas = () => {
  const { username } = useUser();
  const [drawDelay, setDrawDelay] = useState(null);
  const [community, setCommunity] = useState("");
  const [drawColor, setDrawColor] = useState("#000000");

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
          <VStack spacing={0} alignItems="flex-start">
            <Heading w="full">
              Drawing as{" "}
              <chakra.span textDecor="underline" color="primary.500">
                {username}
              </chakra.span>
            </Heading>
            <Text fontSize="lg">Community</Text>
            <Text fontSize="lg">Delay</Text>
          </VStack>
          <Box w="full" h="60vw">
            <ColorGrid drawColor={drawColor} />
          </Box>
        </VStack>
        <VStack display="flex" flexDir="column" w="30%" alignItems="flex-start">
          <FormControl display="inline-flex" alignItems="center">
            <FormLabel
              fontSize="lg"
              fontWeight="bold"
              htmlFor="draw-now-dropdown"
              m={0}
              mr={2}
            >
              Draw Now?
            </FormLabel>
            <Switch
              isChecked={drawDelay === null}
              onChange={() => {
                setDrawDelay((prev) => (prev === null ? 0 : null));
              }}
            />
          </FormControl>
          {drawDelay !== null && (
            <HStack spacing={2}>
              <FormLabel m={0} mr={2}>
                Delay
              </FormLabel>
              <Input
                type="number"
                defaultValue={0}
                step={1}
                onChange={(e) => setDrawDelay(Number(e.target.value))}
              />
              <FormLabel m={0}>seconds</FormLabel>
            </HStack>
          )}
          <FormControl>
            <FormLabel
              fontSize="lg"
              fontWeight="bold"
              htmlFor="color-picker"
              textColor={drawColor}
            >
              Draw Color ({drawColor})
            </FormLabel>
            <SketchPicker
              id="color-picker"
              color={drawColor}
              onChange={(e) => setDrawColor(e.hex)}
              onChangeComplete={(e) => setDrawColor(e.hex)}
            />
          </FormControl>
          <FormControl>
            <FormLabel
              fontSize="lg"
              fontWeight="bold"
              htmlFor="community-input"
            >
              Community
            </FormLabel>
            <Input
              type="text"
              placeholder="Enter community name"
              value={community}
              onChange={(e) => setCommunity(e.target.value)}
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
