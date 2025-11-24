import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext.jsx';
import Login from './components/Login.jsx';
import Register from './components/Register.jsx'; 
import Dashboard from './components/Dashboard.jsx'; // NEW: Import the Dashboard component
import './App.css';

function App() {
  const { isAuthenticated } = useAuth(); 

  return (
    <div className="app-container">
      <Routes>
        
        {/* === Public Routes === */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} /> 
        
        {/* === Protected Route === */}
        <Route 
          path="/dashboard" 
          // FIX: Use the actual Dashboard component
          element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" replace />} 
        />

        {/* === Default/Catch-all Route === */}
        <Route 
          path="*" 
          element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <Navigate to="/login" replace />} 
        />
        
      </Routes>
    </div>
  );
}

export default App;