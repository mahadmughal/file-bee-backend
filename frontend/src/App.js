// App.js
import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./pages/Layout";
import DocumentConversion from "./components/FileConversion";
import ImageConverter from "./pages/converters/ImageConverter";
import DocumentConverter from "./pages/converters/DocumentConverter";
import AudioConverter from "./pages/converters/AudioConverter";
import FontConverter from "./pages/converters/FontConverter";
import SignIn from "./pages/auth/SignIn";
import SignUp from "./pages/auth/SignUp";
import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
            <Layout>
              <DocumentConversion />
            </Layout>
          }
        />
        <Route
          path="/image_converter"
          element={
            <Layout>
              <ImageConverter />
            </Layout>
          }
        />
        <Route
          path="/document_converter"
          element={
            <Layout>
              <DocumentConverter />
            </Layout>
          }
        />
        <Route
          path="/audio_converter"
          element={
            <Layout>
              <AudioConverter />
            </Layout>
          }
        />
        <Route
          path="/font_converter"
          element={
            <Layout>
              <FontConverter />
            </Layout>
          }
        />
        <Route path="/sign_up" element={<SignUp />} />
        <Route path="/sign_in" element={<SignIn />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
