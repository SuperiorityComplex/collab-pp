import React, { useEffect } from "react";
import { Alert, AlertDescription, AlertIcon } from "@chakra-ui/react";

const ErrorBanner = ({ message, show, setShow, duration = 5000, onClose }) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      setShow(false);
      onClose && onClose();
    }, duration);

    return () => {
      clearTimeout(timer);
    };
  }, [duration, onClose]);

  return (
    show && (
      <Alert status="error" variant="left-accent">
        <AlertIcon />
        <AlertDescription>{message}</AlertDescription>
      </Alert>
    )
  );
};

export default ErrorBanner;
