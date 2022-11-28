import React from "react";
import CircularProgress from "@mui/material/CircularProgress";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";

const Loading = () => {
  return (
    <Box>
      <CircularProgress />
      <Typography variant="body1">Loading</Typography>
    </Box>
  );
};

export default Loading;
