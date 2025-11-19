import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom'; // NEW: Import useNavigate
import { useAuth } from '../context/AuthContext.jsx'; 

const Login = () => {
    const { login } = useAuth(); 
    const navigate = useNavigate(); // NEW: Initialize useNavigate
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setLoading(true);

        if (!email || !password) {
            setError("Please enter both email and password.");
            setLoading(false);
            return;
        }

        const result = await login(email, password);

        if (result.success) {
            // FIX: Navigate immediately upon receiving the success signal.
            navigate('/dashboard', { replace: true });
        } else {
            setError(result.error);
        }
        
        setLoading(false);
    };

    return (
        <div className="auth-container" style={{ 
            maxWidth: '400px', 
            margin: '50px auto', 
            padding: '20px', 
            backgroundColor: '#2e2e2e', 
            borderRadius: '8px' 
        }}>
            <h2 style={{ color: '#646cff' }}>User Sign In</h2>
            <p style={{ color: '#888' }}>Already registered? Enter your credentials below.</p>
            
            <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: '15px' }}>
                    <input
                        type="email"
                        placeholder="Email (use: user@example.com)"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                        style={inputStyle}
                    />
                </div>
                <div style={{ marginBottom: '20px' }}>
                    <input
                        type="password"
                        placeholder="Password (use: password)"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        style={inputStyle}
                    />
                </div>
                
                {error && (
                    <div style={{ color: '#ff0000', marginBottom: '15px' }}>
                        {error}
                    </div>
                )}

                <button 
                    type="submit" 
                    disabled={loading}
                    style={buttonStyle}
                >
                    {loading ? 'Authenticating...' : 'Log In'}
                </button>
            </form>
            
            <div style={{ marginTop: '20px', textAlign: 'center' }}>
                <Link to="/register" style={{ color: '#aaa', textDecoration: 'none' }}>
                    Go to Register
                </Link>
            </div>
        </div>
    );
};

// Basic inline styles (You should replace these with a CSS framework)
const inputStyle = {
    width: '100%',
    padding: '10px',
    border: '1px solid #444',
    borderRadius: '4px',
    backgroundColor: '#1a1a1a',
    color: 'white',
    boxSizing: 'border-box'
};

const buttonStyle = {
    width: '100%',
    padding: '10px',
    backgroundColor: '#646cff',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontWeight: 'bold'
};

export default Login;