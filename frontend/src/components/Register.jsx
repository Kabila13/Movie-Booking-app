import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Register = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleRegister = async (e) => {
        e.preventDefault();
        try {
            // This hits your FastAPI /auth/register endpoint
            await axios.post('http://localhost:8000/auth/register', { 
                email, 
                password 
            });
            alert("Registration Successful! Please login.");
            navigate('/login'); // We will build the Login page next
        } catch (err) {
            alert("Registration failed: " + (err.response?.data?.detail || "Unknown error"));
        }
    };

    return (
        <div className="flex items-center justify-center h-screen bg-gray-100">
            <form onSubmit={handleRegister} className="bg-white p-8 rounded shadow-md w-96">
                <h2 className="text-2xl font-bold mb-6 text-center text-blue-600">Create Account</h2>
                <div className="mb-4">
                    <label className="block text-gray-700">Email Address</label>
                    <input 
                        type="email" 
                        className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400" 
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>
                <div className="mb-6">
                    <label className="block text-gray-700">Password</label>
                    <input 
                        type="password" 
                        className="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400" 
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <button type="submit" className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600 transition duration-200">
                    Register
                </button>
                <p className="mt-4 text-center text-sm text-gray-600">
                    Already have an account? <a href="/login" className="text-blue-500 underline">Login here</a>
                </p>
            </form>
        </div>
    );
};

export default Register;