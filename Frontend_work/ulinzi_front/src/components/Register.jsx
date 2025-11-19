import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext.jsx'; 

const Register = () => {
    // Get the register function from context
    const { register } = useAuth(); 
    const navigate = useNavigate();

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);
    const [message, setMessage] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setMessage(null);
        setLoading(true);

        if (!email || !password) {
            setError("Please fill out all fields.");
            setLoading(false);
            return;
        }

        // Call the register function from the AuthContext
        const result = await register(email, password);

        if (result.success) {
            // Success logic is now handled in the AuthContext (redirect to /login)
            setMessage(result.message);
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
            <h2 style={{ color: '#646cff' }}>New User Registration</h2>
            <p style={{ color: '#888' }}>Create an account to access the UlinziMind AI Sentinel.</p>
            
            <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: '15px' }}>
                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                        style={inputStyle}
                    />
                </div>
                <div style={{ marginBottom: '20px' }}>
                    <input
                        type="password"
                        placeholder="Password (min 6 characters)"
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
                {message && (
                    <div style={{ color: '#00ff00', marginBottom: '15px' }}>
                        {message}
                    </div>
                )}

                <button 
                    type="submit" 
                    disabled={loading}
                    style={buttonStyle}
                >
                    {loading ? 'Registering...' : 'Register'}
                </button>
            </form>
            
            <div style={{ marginTop: '20px', textAlign: 'center' }}>
                <Link to="/login" style={{ color: '#aaa', textDecoration: 'none' }}>
                    Already registered? Go to Log In
                </Link>
            </div>
        </div>
    );
};

// Basic inline styles (Copying from Login.jsx for consistency)
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

export default Register;