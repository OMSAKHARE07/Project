// App.jsx
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePage from './components/HomePage';
import ResultPage from './components/SummaryResult';

const App = () => (
  <Routes>
    <Route path="/" element={<HomePage />} />
    <Route path="/result" element={<ResultPage />} />
  </Routes>
);

export default App;

