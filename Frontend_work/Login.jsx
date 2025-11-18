import React, { useState } from 'react';
import { Card, Button, Form, Alert } from 'react-bootstrap';

const Login = ({ onSwitchToRegister, onLoginSuccess }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null); // Corresponds to 'login-status-js'
    const [message, setMessage] = useState(null); // Corresponds to 'login-status-py'
    const [loading, setLoading] = useState(false);

    // Placeholder for Firebase/Backend login logic
    const handleLogin = async (e) => {
        e.preventDefault();
        setError(null);
        setMessage("Logging in...");
        setLoading(true);

        try {
            // --- Placeholder: Integrate Firebase 'signInWithEmailAndPassword' here ---
            // Example:
            // const userCredential = await firebase.auth().signInWithEmailAndPassword(email, password);
            // const token = await userCredential.user.getIdToken(); // Get the JWT
            // onLoginSuccess(token); // Pass token to parent for storage/redirection

            // Mock success response
            setTimeout(() => {
                setMessage(null);
                onLoginSuccess("MOCK_JWT_TOKEN"); // Call success handler
            }, 1500);

        } catch (err) {
            // --- Placeholder: Handle Firebase auth errors (e.g., 'auth/wrong-password') ---
            // Example:
            // setError(`Login failed: ${err.message}`);
            setError("Invalid email or password. Please try again.");
            setMessage(null);

        } finally {
            setLoading(false);
        }
    };

    return (
        <Card className="shadow-sm border-0" style={{ backgroundColor: "#2e2e2e" }}>
            <Card.Header>
                <h4 className="text-primary">User Sign In</h4>
            </Card.Header>
            <Card.Body>
                <p className="card-text text-muted">
                    Already registered? Enter your credentials below.
                </p>
                <Form onSubmit={handleLogin}>
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
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="mb-3 form-control"
                        required
                    />
                    <Button
                        variant="primary" // Matches dbc.Button color="primary"
                        type="submit"
                        className="w-100 mb-3"
                        disabled={loading}
                    >
                        {loading ? 'Authenticating...' : 'Log In'}
                    </Button>
                </Form>
                
                {/* Status messages, matching the Dash IDs/classes */}
                <div id="login-status-js" className="mt-2">
                    {error && <Alert variant="danger">{error}</Alert>}
                </div>
                <div id="login-status-py" className="mt-2 text-light">
                    {message && !error && <Alert variant="light">{message}</Alert>}
                </div>
                
                <Button 
                    variant="link" // Matches dbc.Button color="link"
                    id="to-register-button" 
                    onClick={onSwitchToRegister} 
                    className="mt-3 w-100"
                >
                    Go to Register
                </Button>
            </Card.Body>
        </Card>
    );
};

export default Login;