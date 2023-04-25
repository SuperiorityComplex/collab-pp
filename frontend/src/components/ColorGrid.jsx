import { useEffect, useRef, useState } from "react";
import { Grid, GridItem } from "@chakra-ui/react";
import { UserRequest } from "../grpc_stubs/protos/main_pb";
import client from "../grpc_stubs/PPClient";

function ColorGrid({ drawColor, square, setSquare }) {
  const [colors, setColors] = useState(Array(100).fill("#FFFFFF"));
  const refreshInterval = useRef(null);

  const handleCellClick = (index) => {
    const newColors = [...colors];
    newColors[index] = drawColor;
    setColors(newColors);
    setSquare({
      col: index % 10,
      row: Math.floor(index / 10),
      color: drawColor,
    });
  };

  const getCanvas = () => {
    const userRequest = new UserRequest();
    client.displayCanvas(userRequest, {}, (err, response) => {
      setColors(response.getCanvas().split(","));
    });
  };

  useEffect(() => {
    refreshInterval.current = setInterval(getCanvas, 1000);
    return () => clearInterval(refreshInterval.current);
  }, []);

  return (
    <Grid templateColumns="repeat(10, 1fr)" gap={1} w="full" h="full">
      {colors.map((color, index) => (
        <GridItem
          key={index}
          bg={
            square && square.row * 10 + square.col === index
              ? square.color
              : color
          }
          borderColor="gray.100"
          borderWidth="2px"
          onClick={() => handleCellClick(index)}
        />
      ))}
    </Grid>
  );
}

export default ColorGrid;
