// App.js
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import NavBar from './components/NavBar';
import DocumentConversion from './components/DocumentConversion';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <NavBar />
      <Routes>
        <Route path="/" element={<DocumentConversion />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
