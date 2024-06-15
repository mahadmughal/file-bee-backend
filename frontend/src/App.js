// App.js
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import NavBar from './components/NavBar';
import DocumentConversion from './components/FileConversion';
import ImageConverter from './pages/ImageConverter';
import DocumentConverter from './pages/DocumentConverter';
import AudioConverter from './pages/AudioConverter';
import FontConverter from './pages/FontConverter';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <NavBar />
      <Routes>
        <Route path="/" element={<DocumentConversion />} />
        <Route path="/image_converter" element={<ImageConverter />} />
        <Route path="/document_converter" element={<DocumentConverter />} />
        <Route path="/audio_converter" element={<AudioConverter />} />
        <Route path="/font_converter" element={<FontConverter />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
