// import React from "react";
// import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
// import Home from './Home/Home.jsx';
// import  Chatbot  from "./Chatbot/Chatbot.jsx";

// function App() {
//   return (
//     <Router>
//       <Routes>
//         <Route path="/" element={<Home />} />
//         <Route path="/Chatbot" element={<Chatbot />} />
//       </Routes>
//     </Router>
  
//   );
// }

// export default App;
import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [hospitals, setHospitals] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/hospitals")
      .then(response => setHospitals(response.data))
      .catch(error => console.error("Error fetching data:", error));
  }, []);

  return (
    <div>
      <h1>Hospital Recommendations</h1>
      <ul>
        {hospitals.map((hospital, index) => (
          <li key={index}>
            <h2>{hospital.Name}</h2>
            <p>City: {hospital.City}</p>
            <p>Province: {hospital.Province}</p>
            <p>Address: {hospital.Address}</p>
            <p>Specialization: {hospital.Specialization}</p>
            <p>Phone: {hospital.Phone}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
