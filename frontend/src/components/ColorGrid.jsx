import { useState } from "react";
import { Grid, GridItem } from "@chakra-ui/react";

function ColorGrid({ drawColor }) {
  const [colors, setColors] = useState(Array(100).fill("gray.100"));

  const handleCellClick = (index) => {
    const newColors = [...colors];
    newColors[index] = drawColor;
    setColors(newColors);
  };

  return (
    <Grid templateColumns="repeat(10, 1fr)" gap={1} w="full" h="full">
      {colors.map((color, index) => (
        <GridItem
          key={index}
          bg={color}
          onClick={() => handleCellClick(index)}
        />
      ))}
    </Grid>
  );
}

export default ColorGrid;
