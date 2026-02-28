import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        // 1. STOP the page from refreshing
        e.preventDefault(); 
        
        try {
            const res = await axios.post("http://localhost:8000/auth/login", { email, password });
            
            // 2. Store the data correctly
            localStorage.setItem("token", res.data.access_token);
            localStorage.setItem("is_admin", res.data.is_admin); 

            alert("Login Successful!");
            
            // 3. Use navigate instead of window.location for a smoother feel
            navigate("/dashboard"); 
        } catch (err) {
            console.error(err);
            alert(err.response?.data?.detail || "Invalid Email or Password");
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100">
            <div className="bg-white p-10 rounded-2xl shadow-xl w-full max-w-md text-center">
                <h2 className="text-3xl font-extrabold mb-6 text-gray-900">Sign In</h2>
                
                {/* 4. Ensure onSubmit is calling handleLogin */}
                <form onSubmit={handleLogin} className="space-y-5">
                    <input 
                        type="email" 
                        placeholder="Email Address"
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                        onChange={(e) => setEmail(e.target.value)} 
                        value={email} // Controlled component
                        required 
                    />
                    <input 
                        type="password" 
                        placeholder="Password"
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                        onChange={(e) => setPassword(e.target.value)} 
                        value={password} // Controlled component
                        required 
                    />
                    <button type="submit" className="w-full bg-green-600 hover:bg-blue-700 text-white font-bold py-3 rounded-lg transition-all">
                        Sign In
                    </button>
                </form>
                
                <p className="mt-6 text-gray-600">
                    New here? <Link to="/register" className="text-green-600 hover:underline font-medium">Register here</Link>
                </p>
            </div>
        </div>
    );
};

export default Login;