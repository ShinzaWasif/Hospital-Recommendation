import React, { useState } from "react";
import "./Chatbot.css";
function Chatbot() {
  const [messages, setMessages] = useState([
    { text: "Hello! How can I assist you today?", sender: "bot" }
  ]);
  const [input, setInput] = useState("");

  const sendMessage = () => {
    if (input.trim()) {
      setMessages([...messages, { text: input, sender: "user" }]);
      setInput("");
    }
  };

  return (
    <>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet"></link>
    <section class="text-gray-400 body-font">
    <div className="h-screen flex flex-col  text-white">
      {/* Chatbot Interface */}
      <div className="chat-container flex flex-col flex-1 overflow-y-auto p-4 space-y-3">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`p-3 rounded-lg max-w-xs ${
              msg.sender === "bot"
                ? "self-start bg-gradient-to-r from-green-400 to-blue-500"
                : "self-end bg-gradient-to-r from-blue-500 to-purple-600"
            }`}
          >
            {msg.text}
          </div>
        ))}
      </div>

      {/* Input Box */}
      <div className="p-4 bg-gray-800 border-t flex items-center">
        <input
          type="text"
          placeholder="Type a message..."
          className="flex-1 p-2 border rounded-l-lg bg-gray-700 text-white focus:outline-none"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === "Enter" && sendMessage()}
        />
        <button className=" px-4 py-2 rounded-r-lg text-white zoom-out" onClick={sendMessage}>
          <i className="fa fa-paper-plane text-xl" />
        </button>
      </div>
    </div>
    </section>
    
    </>
  );
}

export default Chatbot;






