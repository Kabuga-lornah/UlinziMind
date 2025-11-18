import React, { useState } from 'react';
import { Card, Button, Form, Alert } from 'react-bootstrap';

// This component assumes you are using React-Bootstrap for styling
// and a separate routing mechanism (like react-router-dom) for navigation.

const Register = ({ onSwitchToLogin }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null); // Corresponds to 'register-status-js'
    const [message, setMessage] = useState(null); // Corresponds to 'register-status-py'
    const [loading, setLoading] = useState(false);

    // Placeholder for Firebase/Backend registration logic
    const handleRegister = async (e) => {
        e.preventDefault();
        setError(null);
        setMessage(null);
        setLoading(true);

        if (password.length < 6) {
            setError("Password must be at least 6 characters.");
            setLoading(false);
            return;
        }

        try {
            // --- Placeholder: Integrate Firebase 'createUserWithEmailAndPassword' here ---
            // Example:
            // const userCredential = await firebase.auth().createUserWithEmailAndPassword(email, password);
            // console.log("User registered:", userCredential.user);

            // Mock success response
            setMessage("Registration successful! Redirecting to login...");
            setTimeout(() => {
                onSwitchToLogin(); // Navigate to the login page on success
            }, 2000);

        } catch (err) {
            // --- Placeholder: Handle Firebase auth errors (e.g., 'auth/email-already-in-use') ---
            // Example:
            // setError(`Registration failed: ${err.message}`);
            setError("Error registering user. Please try again.");

        } finally {
            setLoading(false);
        }
    };

    return (
        <Card className="shadow-sm border-0" style={{ backgroundColor: "#2e2e2e" }}>
            <Card.Header>
                <h4 className="text-primary">New User Registration</h4>
            </Card.Header>
            <Card.Body>
                <p className="card-text text-muted">
                    Create an account to access the UlinziMind AI Sentinel.
                </p>
                <Form onSubmit={handleRegister}>
                    <Form.Control
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className="mb-3 form-control"
                        required
                    />
                    <Form.Control
                        type="password"
                        placeholder="Password (min 6 characters)"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="mb-3 form-control"
                        required
                    />
                    <Button
                        variant="info" // Matches dbc.Button color="info"
                        type="submit"
                        className="w-100 mb-3"
                        disabled={loading}
                    >
                        {loading ? 'Registering...' : 'Register'}
                    </Button>
                </Form>
                
                {/* Status messages, matching the Dash IDs/classes */}
                <div id="register-status-js" className="mt-2">
                    {error && <Alert variant="danger">{error}</Alert>}
                </div>
                <div id="register-status-py" className="mt-2 text-light">
                    {message && <Alert variant="light">{message}</Alert>}
                </div>

                <Button variant="link" onClick={onSwitchToLogin} className="mt-3 w-100">
                    Already registered? Go to Log In
                </Button>
            </Card.Body>
        </Card>
    );
};

export default Register;