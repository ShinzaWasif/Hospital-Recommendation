// import React, { useState, useEffect, useRef } from "react";
// import { useNavigate } from "react-router-dom";
// import "./Chatbot.css";
// import Header from "../Header/Header.jsx";

// function Chatbot() {
//   const [messages, setMessages] = useState([
//     { text: "Hello! How can I assist you today?", sender: "bot" }
//   ]);
//   const [input, setInput] = useState("");
//   const messagesEndRef = useRef(null);

//   const generateBotResponse = (userInput) => {
//     const responses = {
//       "hello": "Hi there! How can I help?",
//       "how are you": "I'm just a bot, but I'm doing great!",
//       "what is your name": "I'm a simple chatbot!",
//       "bye": "Goodbye! Have a great day!"
//     };

//     const lowerInput = userInput.toLowerCase();
//     return responses[lowerInput] || "I'm not sure how to respond to that.";
//   };

//   const sendMessage = () => {
//     if (input.trim()) {
//       const userMessage = { text: input, sender: "user" };
//       const botMessage = { text: generateBotResponse(input), sender: "bot" };
      
//       setMessages((prevMessages) => [...prevMessages, userMessage, botMessage]);
//       setInput("");
//     }
//   };

//   // Auto-scroll to the latest message
//   useEffect(() => {
//     messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
//   }, [messages]);

//   return (
//     <>
//       <Header />
//       <div className="chat-container">
//         {/* Messages */}
//         <div className="chat-messages">
//           {messages.map((msg, index) => (
//             <div key={index} className={msg.sender === "bot" ? "bot-message" : "user-message"}>
//               {msg.text}
//             </div>
//           ))}
//           <div ref={messagesEndRef} />
//         </div>

//         {/* Input Box */}
//         <div id="chatInputContainer">
//           <input
//             type="text"
//             placeholder="Type a message..."
//             id="chatInput"
//             value={input}
//             onChange={(e) => setInput(e.target.value)}
//             onKeyPress={(e) => e.key === "Enter" && sendMessage()}
//           />
//           <button id="sendButton" onClick={sendMessage}>
//             <i className="fa fa-paper-plane text-xl"></i>
//           </button>
//         </div>
//       </div>
//     </>
//   );
// }

// export default Chatbot;

import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import "./Chatbot.css";
import Header from "../Header/Header.jsx";

function Chatbot() {
  const [messages, setMessages] = useState([
    { text: "Hello! Ask me about hospitals in Pakistan.", sender: "bot" }
  ]);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef(null);

  const sendMessage = async () => {
    if (input.trim()) {
      const userMessage = { text: input, sender: "user" };
      setMessages((prevMessages) => [...prevMessages, userMessage]);

      try {
        const response = await fetch("http://127.0.0.1:5000/chatbot", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query: input })
        });

        const data = await response.json();
        const botMessage = { text: data.response, sender: "bot" };
        setMessages((prevMessages) => [...prevMessages, botMessage]);
      } catch (error) {
        setMessages((prevMessages) => [...prevMessages, { text: "Error fetching response.", sender: "bot" }]);
      }

      setInput("");
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <>
      <Header />
      <div className="chat-container">
        <div className="chat-messages">
          {messages.map((msg, index) => (
            <div key={index} className={msg.sender === "bot" ? "bot-message" : "user-message"}>
              {msg.text}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
        <div id="chatInputContainer">
          <input
            type="text"
            placeholder="Ask about hospitals..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && sendMessage()}
          />
          <button id="sendButton" onClick={sendMessage}>
            <i className="fa fa-paper-plane text-xl"></i>
          </button>
        </div>
      </div>
    </>
  );
}

export default Chatbot;
