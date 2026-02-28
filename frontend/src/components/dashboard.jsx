import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Dashboard = () => {
    const [events, setEvents] = useState([]);
    const [myBookings, setMyBookings] = useState([]);
    const [quantities, setQuantities] = useState({});
    
    // --- NEW: Modal and Message States ---
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [statusMessage, setStatusMessage] = useState("");
    const [newMovie, setNewMovie] = useState({ title: '', description: '', total_seats: 100 });

    const isAdmin = localStorage.getItem("is_admin") === "true";

    const fetchData = async () => {
        const token = localStorage.getItem("token");
        const headers = { Authorization: `Bearer ${token}` };
        try {
            const eventsRes = await axios.get("http://localhost:8000/events/", { headers });
            setEvents(eventsRes.data);

            const bookingsRes = await axios.get("http://localhost:8000/bookings/my-bookings", { headers });
            setMyBookings(bookingsRes.data);
        } catch (err) {
            console.error("Fetch failed", err);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    // --- NEW: Function to Create Movie ---
    const handleCreateMovie = async (e) => {
        e.preventDefault();
        const token = localStorage.getItem("token");
        try {
            await axios.post("http://localhost:8000/events/", {
                title: newMovie.title,
                description: newMovie.description,
                total_seats: parseInt(newMovie.total_seats),
                available_seats: parseInt(newMovie.total_seats)
            }, {
                headers: { Authorization: `Bearer ${token}` }
            });

            setStatusMessage("🎬 Movie Listing Created Successfully!");
            setIsModalOpen(false); // Close the popup
            setNewMovie({ title: '', description: '', total_seats: 100 }); // Reset form
            setTimeout(() => setStatusMessage(""), 3000); // Clear message
            fetchData(); // Refresh list
        } catch (err) {
            alert(err.response?.data?.detail || "Creation failed. Admin only.");
        }
    };

    const handleBooking = async (eventId) => {
        const token = localStorage.getItem("token");
        const seatCount = quantities[eventId] || 1;
        try {
            await axios.post(`http://localhost:8000/bookings/book/${eventId}?seats=${seatCount}`, {}, {
                headers: { Authorization: `Bearer ${token}` }
            });
            
            setStatusMessage(`🎉 Booking Successful for ${seatCount} seat(s)!`);
            setTimeout(() => setStatusMessage(""), 3000);
            await fetchData();
        } catch (err) {
            alert(err.response?.data?.detail || "Booking failed.");
        }
    };

    const deleteEvent = async (id) => {
        const token = localStorage.getItem("token");
        if (window.confirm("Admin Alert: Delete this movie?")) {
            try {
                await axios.delete(`http://localhost:8000/events/${id}`, {
                    headers: { Authorization: `Bearer ${token}` }
                });
                setStatusMessage("🗑️ Movie Deleted.");
                setTimeout(() => setStatusMessage(""), 3000);
                fetchData();
            } catch (err) {
                alert("Delete failed.");
            }
        }
    };

    return (
        <div className="p-10 bg-gray-50 min-h-screen text-gray-800">
            
            {/* --- SUCCESS MESSAGE BANNER --- */}
            {statusMessage && (
                <div className="fixed top-5 left-1/2 transform -translate-x-1/2 z-50 bg-green-600 text-white px-8 py-3 rounded-full shadow-2xl font-bold">
                    {statusMessage}
                </div>
            )}

            <h1 className="text-4xl font-extrabold mb-10 text-center">Pinesphere Movie Dashboard</h1>

            {/* --- ADMIN ONLY PANEL (KEPT YELLOW) --- */}
            {isAdmin && (
                <div className="max-w-7xl mx-auto mb-10 bg-yellow-50 border-2 border-yellow-200 p-6 rounded-2xl shadow-sm">
                    <h2 className="text-2xl font-bold text-yellow-800 mb-2">Admin Panel</h2>
                    <p className="mb-4 text-yellow-700">You have management privileges. Be careful with deletions.</p>
                    <button 
                        onClick={() => setIsModalOpen(true)} // Opens the modal
                        className="bg-yellow-600 text-white px-6 py-2 rounded-lg font-bold hover:bg-yellow-700"
                    >
                        + Create New Movie Listing
                    </button>
                </div>
            )}

            {/* --- NEW: CREATE MOVIE MODAL POPUP --- */}
            {isModalOpen && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
                    <div className="bg-white rounded-2xl p-8 max-w-md w-full shadow-2xl text-left">
                        <h2 className="text-2xl font-bold mb-6 text-gray-800">New Movie Listing</h2>
                        <form onSubmit={handleCreateMovie} className="space-y-4">
                            <div>
                                <label className="block text-sm font-bold text-gray-700 mb-1">Title</label>
                                <input 
                                    type="text" required className="w-full p-2 border rounded-lg"
                                    onChange={(e) => setNewMovie({...newMovie, title: e.target.value})}
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-bold text-gray-700 mb-1">Description</label>
                                <textarea 
                                    required className="w-full p-2 border rounded-lg"
                                    onChange={(e) => setNewMovie({...newMovie, description: e.target.value})}
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-bold text-gray-700 mb-1">Total Seats</label>
                                <input 
                                    type="number" required className="w-full p-2 border rounded-lg"
                                    onChange={(e) => setNewMovie({...newMovie, total_seats: e.target.value})}
                                />
                            </div>
                            <div className="flex space-x-3 pt-4">
                                <button type="button" onClick={() => setIsModalOpen(false)} className="flex-1 py-2 bg-gray-200 rounded-lg font-bold">Cancel</button>
                                <button type="submit" className="flex-1 py-2 bg-blue-600 text-white rounded-lg font-bold">Save Movie</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
            
            {/* --- MOVIE GRID --- */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
                {events.map(event => (
                    <div key={event.id} className="bg-white border border-gray-200 p-6 rounded-2xl shadow-md relative">
                        {isAdmin && (
                            <button onClick={() => deleteEvent(event.id)} className="absolute top-3 right-3 text-red-400 hover:text-red-600 font-bold text-sm">✕ Delete</button>
                        )}
                        <h3 className="text-2xl font-bold text-blue-900 mb-2">{event.title}</h3>
                        <p className="text-gray-600 mb-4 h-12 overflow-hidden">{event.description}</p>
                        <div className="bg-blue-50 p-3 rounded-lg mb-4">
                            <p className="text-blue-800 font-medium text-center">🎟️ Seats: <span className="font-bold">{event.available_seats}</span> / {event.total_seats}</p>
                        </div>
                        {!isAdmin && (
                            <>
                                <input 
                                    type="number" min="1" max={event.available_seats}
                                    value={quantities[event.id] || 1}
                                    onChange={(e) => setQuantities({...quantities, [event.id]: parseInt(e.target.value) || 1})}
                                    className="w-full p-2 border border-gray-300 rounded-lg mb-4"
                                />
                                <button 
                                    onClick={() => handleBooking(event.id)}
                                    disabled={event.available_seats <= 0}
                                    className={`w-full font-bold py-3 rounded-xl ${event.available_seats > 0 ? "bg-blue-600 text-white" : "bg-gray-300 text-gray-500"}`}
                                >
                                    {event.available_seats > 0 ? `Book ${quantities[event.id] || 1} Ticket(s)` : "Sold Out"}
                                </button>
                            </>
                        )}
                    </div>
                ))}
            </div>

            {/* --- BOOKING HISTORY --- */}
            {!isAdmin && (
                <div className="max-w-4xl mx-auto mt-20 pb-20">
                    <h2 className="text-3xl font-bold mb-8 text-center">My Confirmed Tickets</h2>
                    <div className="space-y-4">
                        {myBookings.length > 0 ? (
                            myBookings.map(ticket => (
                                <div key={ticket.id} className="bg-white border-l-8 border-green-500 p-5 rounded-xl shadow-sm flex justify-between items-center">
                                    <div>
                                        <h4 className="font-bold text-xl text-gray-900">{ticket.event_title || "Ticket"}</h4>
                                        <p className="text-gray-500 text-sm">#PS-{ticket.id}</p>
                                    </div>
                                    <span className="bg-green-100 text-green-700 px-4 py-2 rounded-full text-xs font-black uppercase">Confirmed</span>
                                </div>
                            ))
                        ) : (
                            <p className="text-center text-gray-500 italic">No tickets found.</p>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default Dashboard;