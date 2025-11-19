import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext.jsx';
import Login from './components/Login.jsx';
import Register from './components/Register.jsx'; // NEW: Import the Register component
import './App.css';

// Placeholder components (replace with actual components later)
const DashboardPage = () => {
    const { logout } = useAuth();
    return (
        <div style={{ padding: '20px' }}>
            <h1>Dashboard - Protected Content</h1>
            <p>You are successfully logged in and ready to view real-time intelligence data!</p>
            <button onClick={logout} style={{ padding: '10px', backgroundColor: '#888' }}>
                Log Out
            </button>
        </div>
    );
};


function App() {
  const { isAuthenticated } = useAuth(); 

  return (
    <div className="app-container">
      <Routes>
        
        {/* === Public Routes === */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} /> {/* Use the actual Register component */}
        
        {/* === Protected Route === */}
        <Route 
          path="/dashboard" 
          element={isAuthenticated ? <DashboardPage /> : <Navigate to="/login" replace />} 
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