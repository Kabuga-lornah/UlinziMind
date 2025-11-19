import { createContext, useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { initializeApp } from 'firebase/app'; // New Import
import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword, signOut } from 'firebase/auth'; // New Auth Imports

// 1. YOUR FIREBASE CONFIGURATION (From your screenshot)
const firebaseConfig = {
  apiKey: "AIzaSyDU_xPuE1EkpGGvFae2nH9_khctiV5dUJY",
  authDomain: "ulinzimind.firebaseapp.com",
  projectId: "ulinzimind",
  storageBucket: "ulinzimind.firebaseapp.com",
  messagingSenderId: "716679595914",
  appId: "1:716679595914:web:e02b5c137e514246156a73",
  measurementId: "G-BTZH80JN16"
};

// 2. Initialize Firebase and Authentication Service
const app = initializeApp(firebaseConfig);
const auth = getAuth(app); // Get the Authentication service instance

// Create the Context
const AuthContext = createContext(null);

export const useAuth = () => {
  return useContext(AuthContext);
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null); 
  const [token, setToken] = useState(localStorage.getItem('token')); 
  const [isAuthenticated, setIsAuthenticated] = useState(!!token);
  const navigate = useNavigate();

  useEffect(() => {
    // This listener automatically manages user state changes from Firebase
    const unsubscribe = auth.onAuthStateChanged(firebaseUser => {
      if (firebaseUser) {
        firebaseUser.getIdToken().then(idToken => {
          localStorage.setItem('token', idToken);
          setToken(idToken);
          setIsAuthenticated(true);
          setUser(firebaseUser);
        });
      } else {
        localStorage.removeItem('token');
        setToken(null);
        setIsAuthenticated(false);
        setUser(null);
      }
    });
    return () => unsubscribe();
  }, []);

  // --- Authentication Functions ---

  const login = async (email, password) => {
    try {
      // Use Firebase SDK to sign in
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      
      // If successful, the onAuthStateChanged listener handles state/token updates.
      return { success: true };
    } catch (error) {
      console.error("Firebase Login Error:", error);
      // Return a user-friendly error message
      return { success: false, error: "Invalid email or password." };
    }
  };

  const register = async (email, password) => {
    try {
        // Use Firebase SDK to create a new user
        const userCredential = await createUserWithEmailAndPassword(auth, email, password);
        
        // After creation, log the user out and redirect to login
        await auth.signOut();
        navigate('/login', { replace: true });
        return { success: true, message: "Registration successful! You may now log in." };
    } catch (error) {
        console.error("Firebase Registration Error:", error);
        let errorMessage = "Registration failed.";
        if (error.code === 'auth/email-already-in-use') {
            errorMessage = "This email is already registered.";
        }
        return { success: false, error: errorMessage };
    }
  };


  const logout = async () => {
    await signOut(auth); // Use Firebase SDK to sign out
    // The onAuthStateChanged listener handles the rest of the state cleanup.
    navigate('/login', { replace: true });
  };

  // ⚠️ IMPORTANT: The login/logout redirects are now handled by React Router in App.jsx,
  // triggered by the isAuthenticated state change (via onAuthStateChanged).
  const contextValue = {
    isAuthenticated,
    user,
    token,
    login,
    logout,
    register,
    // Provide Firebase instance directly if needed for other services
    // firebaseApp: app, 
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};