// App.js
import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import AuthProvider from "./contexts/AuthContext";
import { AlertProvider } from "./contexts/Alert";
import Layout from "./pages/Layout";
import FileConversion from "./components/FileConversion";
import ImageConverter from "./pages/converters/ImageConverter";
import DocumentConverter from "./pages/converters/DocumentConverter";
import AudioConverter from "./pages/converters/AudioConverter";
import FontConverter from "./pages/converters/FontConverter";
import SignIn from "./pages/auth/SignIn";
import SignUp from "./pages/auth/SignUp";
import ResetPassword from "./pages/auth/ResetPassword";
import HelpRequest from "./pages/HelpRequest";
import Profile from "./pages/Profile";
import Help from "./pages/Help";
import Api from "./pages/Api";
import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AlertProvider>
          <Routes>
            <Route
              path="/"
              element={
                <Layout>
                  <FileConversion />
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
            <Route path="/api" element={<Api />} />
            {/* Nested routes for Help */}
            <Route path="/help" element={<Layout />}>
              <Route index element={<Help />} />
              <Route path="submit_request" element={<HelpRequest />} />
            </Route>

            <Route path="/sign_up" element={<SignUp />} />
            <Route path="/sign_in" element={<SignIn />} />
            <Route path="/reset_password" element={<ResetPassword />} />
            <Route path="/reset_password/:token" element={<ResetPassword />} />
            <Route
              path="/profile"
              element={
                <Layout>
                  <Profile />
                </Layout>
              }
            />
          </Routes>
        </AlertProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
