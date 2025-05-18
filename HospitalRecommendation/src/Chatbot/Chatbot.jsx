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
  const recognitionRef = useRef(null);

  // Function to handle speech input
  const startListening = () => {
    if (!('webkitSpeechRecognition' in window)) {
      alert("Speech recognition is not supported in your browser.");
      return;
    }

    const recognition = new window.webkitSpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onresult = (event) => {
      const speechText = event.results[0][0].transcript;
      setInput(speechText); // Fill input with speech-to-text result
    };
    
    recognition.onerror = (event) => {
      console.error("Speech recognition error:", event.error);
    };
    
    recognitionRef.current = recognition;
    recognition.start();
  };

  const sendMessage = async () => {
    if (input.trim()) {
      const feeRegex = /fee:\s*(\d+\s*-\s*\d+)/i;
      const feeMatch = input.match(feeRegex);
      const extractedFeeRange = feeMatch ? feeMatch[1] : "";
      const cleanedQuery = input.replace(feeRegex, "").trim();

      const userMessage = { text: input, sender: "user" };
      setMessages((prevMessages) => [...prevMessages, userMessage]);

      try {
        const response = await fetch("http://127.0.0.1:5000/chatbot", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query: cleanedQuery, feeRange: extractedFeeRange })
        });

        const data = await response.json();
        const hospitals = Array.isArray(data.response) ? data.response : [];

        setMessages((prevMessages) => [
          ...prevMessages,
          hospitals.length > 0
            ? { hospitals, sender: "bot" }
            : { text: "Sorry, no matching hospitals found.", sender: "bot" }
        ]);
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
          {messages.map((msg, index) => {
            if (msg.sender === "bot" && msg.hospitals) {
              return (
                <div key={index} className="hospital-list">
                  {msg.hospitals.map((hospital, idx) => (
                    <div key={idx} className="hospital-card">
                      <h3>{hospital["Name"]}</h3>
                      <p><strong>City:</strong> {hospital["City"]}</p>
                      <p><strong>Province:</strong> {hospital["Province"]}</p>
                      <p><strong>Specialization:</strong> {hospital["Specialization"]}</p>
                      <p><strong>Phone:</strong> {hospital["Phone"]}</p>
                      <p><strong>Contact Person:</strong> {hospital["ContactPerson"]}</p>
                      <p><strong>Address:</strong> {hospital["Address"]}</p>
                      <p><strong>Fees:</strong> {hospital["Fees"]}</p>
                      <p><strong>Website:</strong> 
                        {hospital["Website"] ? <a href={hospital["Website"]} target="_blank" rel="noopener noreferrer"> Visit</a> : "Not Available"}
                      </p>
                    </div>
                  ))}
                </div>
              );
            } else {
              return (
                <div key={index} className={msg.sender === "bot" ? "bot-message" : "user-message"}>
                  {msg.text}
                </div>
              );
            }
          })}
          <div ref={messagesEndRef} />
        </div>
        {/* <div id="chatInputContainer">
          <input
            type="text"
            placeholder='Ask about hospitals... (e.g., "Cancer hospitals in Lahore fee: 50000-60000")'
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && sendMessage()}
          />
          <button id="micButton" onClick={startListening}>
            <i className="fa fa-microphone text-xl"></i>
          </button>
          <button id="sendButton" onClick={sendMessage}>
            <i className="fa fa-paper-plane text-xl"></i>
          </button>
        </div> */}
      </div>
      <div id="chatInputContainer">
  <input
    id="chatInput"
    type="text"
    placeholder='Ask about hospitals... (e.g., "Cancer hospitals in Lahore fee: 50000-60000")'
    value={input}
    onChange={(e) => setInput(e.target.value)}
    onKeyPress={(e) => e.key === "Enter" && sendMessage()}
  />
  <button id="micButton" onClick={startListening}>
    <i className="fa fa-microphone text-xl"></i>
  </button>
  <button id="sendButton" onClick={sendMessage}>
    <i className="fa fa-paper-plane text-xl"></i>
  </button>
</div>


    </>
  );
}

export default Chatbot;