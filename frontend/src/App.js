import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { HelmetProvider, Helmet } from "react-helmet-async";
import AnomalyDetection from "./pages/AnomalyDetection";
import Footer from "./components/Footer";

function App() {
  return (
    <HelmetProvider>
      <Helmet
        titleTemplate="%s | Anomaly Detection"
        defaultTitle="Anomaly Detection"
      />
      <BrowserRouter>
        <Routes>
          <Route exact path="/" element={<AnomalyDetection />} />
        </Routes>
      </BrowserRouter>
      <Footer />
    </HelmetProvider>
  );
}

export default App;
