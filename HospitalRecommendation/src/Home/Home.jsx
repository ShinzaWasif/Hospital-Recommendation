import React from "react";
import { useNavigate } from "react-router-dom";
import "./Home.css";


function Home() {
  const navigate = useNavigate();
  return (
    <>
 
    <link rel="shortcut icon" href="./public/PredictMed Logo.png" type="image/x-icon"></link>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet"></link>
   

  <section class="text-gray-400 body-font">
    <div class="container mx-auto flex px-5 py-24 md:flex-row flex-col items-center">
      <div class="lg:flex-grow md:w-1/2 lg:pr-24 md:pr-16 flex flex-col md:items-start md:text-left mb-16 md:mb-0 items-center text-center">
        <h1 class="title-font sm:text-4xl text-3xl mb-4 font-bold text-blue-400">Find Your Nearest
          <br class="hidden lg:inline-block"/>Hospital with PredictMED!
        </h1>
        <p class="mb-8 leading-relaxed text-white">Discovering nearby hospitals is made effortless with our interactive website. Navigate seamlessly through a map interface that pinpoints hospitals in your vicinity, providing detailed information such as services offered, contact details, and directions. Whether you need emergency care or routine medical services, our platform ensures you find the closest healthcare facility quickly and efficiently.</p>
        <div class="flex justify-center">
          {/* <a href="chatbot.jsx" class="inline-flex">
            <button class="text-white bg-gradient-to-r from-green-400 to-blue-500 border-0 py-2 px-6 focus:outline-none hover:from-green-500 hover:to-blue-600 rounded text-lg transform hover:scale-105 transition duration-300 ease-in-out">
              Locate Now!
            </button>
          </a>   */}
           <button 
      onClick={() => navigate("/MainChatbot")}
      className="text-white bg-gradient-to-r from-green-400 to-blue-500 border-0 py-2 px-6 focus:outline-none hover:from-green-500 hover:to-blue-600 rounded text-lg transform hover:scale-105 transition duration-300 ease-in-out"
    >
      Locate Now!
    </button>
        </div>
      </div>
       <div className="video-section">
             <video className="object-cover object-center rounded-full w-full md:h-auto md:w-96" style={{ filter: 'blend(screen)' }} loop autoPlay muted>
              <source src="./public/locationvid.mp4" type="video/mp4" />
           </video>
          </div>
    </div>
  </section>
 
    </>
  );
};


export default Home;

