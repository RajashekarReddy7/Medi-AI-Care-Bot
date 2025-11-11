import React from "react";
import { FaUserMd, FaMoon, FaSun } from "react-icons/fa";

const Navbar = ({ darkMode, setDarkMode }) => {
  return (
    <nav className="flex justify-between items-center px-6 py-4 bg-blue-700 dark:bg-blue-800 shadow-md text-white">
      <div className="flex items-center space-x-3">
        <FaUserMd className="text-2xl" />
        <h1 className="text-xl font-bold">Doctor Triage AI</h1>
      </div>

      <div className="flex items-center space-x-4">
        <button
          onClick={() => setDarkMode(!darkMode)}
          className="p-2 rounded-md hover:bg-blue-600 transition-all"
        >
          {darkMode ? <FaSun /> : <FaMoon />}
        </button>
        <img
          src="https://i.pravatar.cc/40"
          alt="profile"
          className="w-9 h-9 rounded-full border-2 border-white"
        />
      </div>
    </nav>
  );
};

export default Navbar;
