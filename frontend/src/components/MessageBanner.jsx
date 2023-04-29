import React from "react";
import { Alert, AlertDescription, AlertIcon } from "@chakra-ui/react";

const MessageBanner = ({ message, type = "error" }) => {
  return (
    <Alert status={type} variant="left-accent" zIndex={999}>
      <AlertIcon />
      <AlertDescription>{message}</AlertDescription>
    </Alert>
  );
};

export default MessageBanner;
