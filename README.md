🎬 Pinesphere Movie Booking System
A full-stack movie ticket booking application designed with a seamless user experience and robust administrative controls. Built using FastAPI for a high-performance backend and React (Vite) for a modern, responsive frontend.

🚀 Project Overview
This platform allows users to browse currently showing movies, select ticket quantities, and book seats in real-time. It also features a dedicated Admin Panel for movie management.

✨ Key Features
Role-Based Access Control (RBAC): Distinct interfaces for Admins and regular Users.

Real-Time Seat Management: Seat availability updates automatically upon successful booking.

Admin Dashboard: Exclusive access to create new movie listings and delete outdated ones.

Booking History: Users can view their confirmed tickets with unique reference IDs.
Interactive UI: Built with Tailwind CSS, featuring success notification banners for instant feedback.

🛠️ Tech Stack
Frontend: React.js (Vite), Tailwind CSS, Axios.

Backend: FastAPI (Python), JWT Authentication.

Database: SQLAlchemy (SQLite/PostgreSQL).

Version Control: Git & GitHub.
📦 Installation & Setup
1. Backend Setup
Bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
2. Frontend Setup
Bash
cd frontend
npm install
npm run dev
📸 Preview
Note: You can upload the screenshots you shared with me into a screenshots/ folder in your repo to show off the UI!

User Dashboard: Browsing and booking tickets.

Admin Panel: Yellow-themed management console for privileged actions.

Success Alerts: Green notification banners confirming transactions.

🛡️ Security
The application uses JWT (JSON Web Tokens) stored in localStorage to handle secure sessions and differentiate between Admin and User permissions.
