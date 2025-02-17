
// import React from "react";
// import { useNavigate } from "react-router-dom";
// import "./Header.css";


// function Header() {
//   const navigate = useNavigate();
//   return (
//     <>
//     <link rel="shortcut icon" href="./public/PredictMed Logo.png" type="image/x-icon"></link>
//     <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet"></link>
//   <header class="w-full flex justify-between items-center p-6 shadow-sm bg-gradient-healthcare">
//     <div class="flex items-center space-x-2">
//       <img src="./public/PredictMed Logo.png" alt="PredictMed Logo" class="h-10 w-10 rounded-full"/>
//       {/* <span class="text-2xl font-bold text-white">Predict<span class="text-purple-300"/>MED</span> */}
//       <p class="text-2xl font-bold text-white">Predict</p><p class="text-2xl font-bold text-purple-300">MED</p>
//     </div>
//     <div>
//       <nav class="flex space-x-4"> 
//     <button  
//       onClick={() => navigate("/")}
//     class="font-bold text-white hover:text-purple-300">Home</button>
//     </nav>
//     </div>
    
//   </header>
 
//     </>
//   );
// };


// export default Header;


import React from "react";
import { useNavigate } from "react-router-dom";
import "./Header.css";

function Header() {
  const navigate = useNavigate();
  return (
    <>
      <header className="w-full flex justify-between items-center p-6 bg-gradient-healthcare">
        {/* Logo & Branding */}
        <div className="logo">
          <img src="./public/PredictMed Logo.png" alt="PredictMed Logo" />
          <div className="branding">
            <p className="predict">Predict</p>
            <p className="med">MED</p>
          </div>
        </div>

        {/* Navigation */}
        <nav>
          <button onClick={() => navigate("/")}>Home</button>
        </nav>
      </header>
    </>
  );
}

export default Header;

