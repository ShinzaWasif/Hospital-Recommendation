import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from './Home/Home.jsx';
import  Chatbot  from "./Chatbot/Chatbot.jsx";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/Chatbot" element={<Chatbot />} />
      </Routes>
    </Router>
  
  );
}

export default App;

