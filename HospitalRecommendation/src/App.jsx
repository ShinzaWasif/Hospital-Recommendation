// import { useState } from 'react'
// import './App.css'
// import  MainChatbot  from "./Chatbot/MainChatbot.jsx";
// import MainHome from './Home/MainHome.jsx';

// function App() {

//   return (
//     <>
//     {/* <Header></Header> */}
//     {/* <Home /> */}
//     {/* <Chatbot /> */}
//     <MainHome/>
//     <MainChatbot />
//     </>
//   )
// }

// export default App

import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import  MainChatbot  from "./Chatbot/MainChatbot.jsx";
import MainHome from './Home/MainHome.jsx';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainHome />} />
        <Route path="/MainChatbot" element={<MainChatbot />} />
      </Routes>
    </Router>
  );
}

export default App;

