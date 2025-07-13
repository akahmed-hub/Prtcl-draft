import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Box, Container } from '@mui/material';

import Layout from './components/Layout/Layout';
import Dashboard from './pages/Dashboard/Dashboard';
import ProtocolBuilder from './pages/ProtocolBuilder/ProtocolBuilder';
import DataAnalysis from './pages/DataAnalysis/DataAnalysis';
import Visualization from './pages/Visualization/Visualization';
import Login from './pages/Auth/Login';
import Register from './pages/Auth/Register';

function App() {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Routes>
        {/* Auth routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        
        {/* Protected routes */}
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="protocols" element={<ProtocolBuilder />} />
          <Route path="analysis" element={<DataAnalysis />} />
          <Route path="visualization" element={<Visualization />} />
        </Route>
      </Routes>
    </Box>
  );
}

export default App; 