import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './chatbot.css'; // Import the CSS file

const axiosConfig = {
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'ca08d70067243e150c4cd95efe5ff884510a8b512c47bd950a6606350f4b03ad', // Include the secret token here
    }
};

function HomePage() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const chatWindowRef = useRef(null); // Create a ref for the chat window

    const sampleQueries = [
        "What's the current stock price of AAPL?",
        "Can you advise me on a home loan?",
        "Tell me about the market capitalization of GOOGL"
    ];

    const handleSend = async (query = input) => {
        if (query.trim() === '') return; // Ignore empty input

        const userMessage = { text: query, sender: 'user' };

        try {
            const response = await axios.post('/api/chat', {
                message: query,
            }, axiosConfig);
            const botMessage = { text: response.data.response, sender: 'bot' };

            // Update state with both messages at once
            setMessages(prevMessages => [...prevMessages, userMessage, botMessage]);
            setInput('');
        } catch (error) {
            console.error('Error sending message to the bot:', error);
            // Even if there is an error, add the user message to the state
            setMessages(prevMessages => [...prevMessages, userMessage]);
        }
    };

    const handleKeyDown = (event) => {
        if (event.key === 'Enter') {
            handleSend();
        }
    };

    const handleSampleQueryClick = (query) => {
        handleSend(query);
    };

    useEffect(() => {
        // Scroll to the bottom of the chat window when messages change
        if (chatWindowRef.current) {
            chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
        }
    }, [messages]);

    return (
        <div className="chatbot-container">
            <h1>Fi-chatbot</h1>
            <div className="sample-queries">
                <p>Try asking:</p>
                {sampleQueries.map((query, index) => (
                    <button key={index} onClick={() => handleSampleQueryClick(query)} className="sample-query">
                        {query}
                    </button>
                ))}
            </div>
            <div className="chat-window" ref={chatWindowRef}>
                {messages.map((msg, index) => (
                    <div key={index} className={`message message-${msg.sender}`}>
                        <p>{msg.text}</p>
                    </div>
                ))}
            </div>
            <div className="input-container">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    className="chat-input"
                />
                <button onClick={() => handleSend()} className="send-button">Send</button>
            </div>
        </div>
    );
}

export default HomePage;
