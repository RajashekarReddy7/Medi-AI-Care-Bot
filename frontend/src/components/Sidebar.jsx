import React from "react";
import { FaHome, FaComments, FaUsers } from "react-icons/fa";

const Sidebar = ({ activePage, setActivePage }) => {
  const navItems = [
    { id: "dashboard", icon: <FaHome />, label: "Dashboard" },
    { id: "chat", icon: <FaComments />, label: "AI Chat" },
    { id: "patients", icon: <FaUsers />, label: "Patients" },
  ];

  return (
    <aside className="w-56 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col py-6">
      {navItems.map((item) => (
        <button
          key={item.id}
          onClick={() => setActivePage(item.id)}
          className={`flex items-center px-6 py-3 text-left space-x-3 hover:bg-blue-100 dark:hover:bg-blue-900 transition-all ${
            activePage === item.id
              ? "bg-blue-50 dark:bg-blue-800 text-blue-600"
              : ""
          }`}
        >
          {item.icon}
          <span className="font-medium">{item.label}</span>
        </button>
      ))}
    </aside>
  );
};

export default Sidebar;
