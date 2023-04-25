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
  Flex,
  IconButton,
  Card,
} from "@chakra-ui/react";
import { SketchPicker } from "react-color";
import { BsChevronDown, BsChevronUp } from "react-icons/bs";
import ColorGrid from "../components/ColorGrid";
import MessageBanner from "../components/MessageBanner";
import Layout from "../components/Layout";
import { useUser } from "../context/UserContext";
import { useRef, useState } from "react";
import { UserRequest } from "../grpc_stubs/protos/main_pb";
import client from "../grpc_stubs/PPClient";

const Canvas = () => {
  const { username } = useUser();
  const [serverMsg, setServerMsg] = useState(null);
  const [drawDelay, setDrawDelay] = useState(null);
  const [community, setCommunity] = useState("");
  const [drawColor, setDrawColor] = useState("#000000");
  const [isOpen, setIsOpen] = useState(true);
  const [drawSquare, setDrawSquare] = useState(null);
  const messageTimer = useRef(null);

  const setServerMsgWrapper = (msg) => {
    clearTimeout(messageTimer.current);
    setServerMsg(msg);
    messageTimer.current = setTimeout(() => {
      setServerMsg(null);
    }, 1000);
  };

  const checkDelay = () => {
    const request = new UserRequest();
    request.setUsername(username);
    client.checkActionDelay(request, {}, (err, response) => {
      setServerMsgWrapper(response.getMessage());
    });
  };

  const checkCommunity = () => {
    const request = new UserRequest();
    request.setUsername(username);
    client.checkCommunity(request, {}, (err, response) => {
      setServerMsgWrapper(response.getMessage());
    });
  };

  const createCommunity = () => {
    // TODO: Error thrown on the backend
    const request = new UserRequest();
    request.setUsername(username);
    request.setCommunity(community);
    client.joinCommunity(request, {}, (err, response) => {
      setServerMsgWrapper(response.getMessage());
    });
  };

  const draw = (isCommunity = false) => {
    if (!drawSquare) {
      setServerMsgWrapper("Please select a square to draw on");
      return;
    }
    const request = new UserRequest();
    request.setUsername(username);
    request.setColor(drawSquare.color);
    request.setRow(drawSquare.row);
    request.setCol(drawSquare.col);
    if (isCommunity) {
      client.joinCommunityTransaction(request, {}, (err, response) => {
        setServerMsgWrapper(response.getMessage());
      });
      return;
    }
    if (drawDelay !== null) {
      request.setDelay(drawDelay);
      client.delayedAction(request, {}, (err, response) => {
        setServerMsgWrapper(response.getMessage());
      });
    } else {
      client.normalAction(request, {}, (err, response) => {
        setServerMsgWrapper(response.getMessage());
      });
    }
  };

  return (
    <Layout>
      {serverMsg && <MessageBanner type="info" message={serverMsg} />}
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
              {username}
            </chakra.span>
          </Heading>
          <Box w="full" h="60vw">
            <ColorGrid
              drawColor={drawColor}
              square={drawSquare}
              setSquare={setDrawSquare}
            />
          </Box>
        </VStack>
        <VStack
          display="flex"
          flexDir="column"
          w="30%"
          alignItems="flex-start"
          spacing={3}
        >
          <Card w="100%" p={2}>
            <Flex
              justify="space-between"
              align="center"
              onClick={() => setIsOpen((prev) => !prev)}
            >
              <Heading size="md">Actions Panel</Heading>
              <IconButton
                icon={isOpen ? <BsChevronUp /> : <BsChevronDown />}
                aria-label={isOpen ? "Close panel" : "Open panel"}
                variant="ghost"
              />
            </Flex>
            {isOpen && (
              <HStack mt={4} spacing={4}>
                <Button onClick={checkDelay}>Check Delay</Button>
                <Button onClick={checkCommunity}>Check Community</Button>
              </HStack>
            )}
          </Card>
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
          <Box h={10} />
          <HStack spacing={2}>
            <Button colorScheme="primary" onClick={() => draw(false)}>
              Draw Now
            </Button>
            <Button
              colorScheme="primary"
              variant="outline"
              onClick={() => draw(true)}
            >
              Add to Community Commit
            </Button>
          </HStack>
          <VStack w="full">
            <Divider my="5" />
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
            <Button colorScheme="primary" onClick={createCommunity}>
              Create Community
            </Button>
          </VStack>
        </VStack>
      </Box>
    </Layout>
  );
};

export default Canvas;
