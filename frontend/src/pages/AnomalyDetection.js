import React, { useEffect, useState } from "react";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import axios from "axios";
import { buttonStyle, imageStyle, boxStyle } from "../styles/styles";
import Loading from "../components/Loading";

function AnomalyDetection() {
  const [uploadedImg, setUploadedImg] = useState();
  const [showResult, setShowResult] = useState(false);
  const [preview, setPreview] = useState(null);
  const [defect, setDefect] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (!uploadedImg) {
      setPreview(null);
      return () => {};
    }

    const imageURL = URL.createObjectURL(uploadedImg);
    setPreview(imageURL);
    console.log(imageURL);
    // Run Back-end to get prediction
    const headers = {
      accept: "application/json",
    };

    const formData = new FormData();
    formData.append("image", uploadedImg);
    setIsLoading(true);
    axios
      .post("http://127.0.0.1:8000/api/detector/", formData, {
        headers: headers,
      })
      .then((response) => {
        getImageResult(response.data.id);
      })
      .catch((err) => console.log(err));
    return () => URL.revokeObjectURL(imageURL);
  }, [uploadedImg]);

  const getImageResult = (id) => {
    axios.get(`http://127.0.0.1:8000/api/detector/${id}/`).then((response) => {
      setDefect(response.data.result);
      setShowResult(true);
      setIsLoading(false);
    });
  };

  const onUpload = (e) => {
    console.log(e.target.files);
    setUploadedImg(e.target.files[0]);
    if (e.target.files.length === 0) {
      return;
    }
    setShowResult(false);
  };

  const upload = () => {
    document.getElementById("inputImage").click();
  };

  return (
    <Grid textAlign="center">
      <Grid item xs={12}>
        <Button variant="contained" sx={buttonStyle} onClick={upload}>
          <Typography variant="h6">UPLOAD</Typography>
        </Button>
        <input
          id="inputImage"
          accept="image/*"
          type="file"
          hidden
          onChange={onUpload}
        />
      </Grid>
      <Grid item xs={12}>
        <Box sx={boxStyle}>
          {preview && <img style={imageStyle} src={preview} alt="Invalid" />}
        </Box>
      </Grid>
      {showResult ? (
        <Grid
          item
          container
          direction="row"
          justifyContent="center"
          spacing={2}
        >
          <Grid item>
            <Typography variant="h4">Detection Result : </Typography>
          </Grid>
          <Grid item>
            {defect ? (
              <Typography variant="h4" color="red">
                Has Defect
              </Typography>
            ) : (
              <Typography variant="h4" color="green">
                No Defect
              </Typography>
            )}
          </Grid>
        </Grid>
      ) : (
        isLoading && <Loading />
      )}
    </Grid>
  );
}

export default AnomalyDetection;
