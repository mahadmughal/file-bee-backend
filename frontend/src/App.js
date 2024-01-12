// App.js
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import NavBar from './components/NavBar';
import UploadFile from './components/UploadFile';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <NavBar />
      <Routes>
        <Route path="/" element={<UploadFile />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
