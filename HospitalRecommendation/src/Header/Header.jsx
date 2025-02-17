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

