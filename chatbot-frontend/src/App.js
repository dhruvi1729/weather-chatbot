import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  // Fetch chat history on component load
  useEffect(() => {
    const fetchChatHistory = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/chat");
        const chatHistory = response.data;
        setMessages(chatHistory);
      } catch (error) {
        console.error("Error fetching chat history", error);
      }
    };

    fetchChatHistory();
  }, []);

  // Function to handle sending a message
  const sendMessage = async () => {
    if (input.trim() === "") return;

    const userMessage = { sender: "user", text: input };
    setMessages([...messages, userMessage]);

    try {
      // Sending message to backend (POST request)
      const response = await axios.post("http://127.0.0.1:5000/chat", { message: input });
      const botMessage = { sender: "bot", text: response.data.reply };
      setMessages([...messages, userMessage, botMessage]);
    } catch (error) {
      const errorMessage = { sender: "bot", text: "Error connecting to the server." };
      setMessages([...messages, userMessage, errorMessage]);
    }

    setInput(""); // Clear the input field after sending
  };

  return (
    <div className="chat-container">
      <div className="chat-box">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            {msg.text}
          </div>
        ))}
      </div>
      <div className="input-box">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

export default App;

