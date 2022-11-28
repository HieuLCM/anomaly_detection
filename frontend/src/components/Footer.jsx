import React from "react";
import Divider from "@mui/material/Divider";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Link from "@mui/material/Link";
import { footerStyle, dividerStyle, textFooterStyle } from "../styles/styles";

const Footer = () => {
  return (
    <Box sx={footerStyle}>
      <Divider sx={dividerStyle} />
      <Typography variant="body1" color="text.secondary" sx={textFooterStyle}>
        {"Model is trained by using the "}
        <Link
          color="inherit"
          href="https://www.mvtec.com/company/research/datasets/mvtec-ad/"
        >
          MVTec Anomaly Detection Dataset
        </Link>
      </Typography>
    </Box>
  );
};

export default Footer;
