import React, { useState } from "react";
import axios from "axios";
import { FaPaperPlane } from "react-icons/fa";

const ChatPanel = () => {
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Hello! I'm your medical assistant. What symptoms are you experiencing?",
    },
  ]);
  const [input, setInput] = useState("");
  const sessionId =
    "session_" + (localStorage.getItem("session_id") || Date.now());

  const sendMessage = async () => {
    if (!input.trim()) return;
    const newMessages = [...messages, { sender: "user", text: input }];
    setMessages(newMessages);
    setInput("");

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/api/chat",
        { session_id: sessionId, message: input },
        { headers: { "Content-Type": "application/json" } }
      );
      const reply =
        res.data.reply || "Please describe your symptoms more clearly.";
      setMessages((m) => [...m, { sender: "bot", text: reply }]);
    } catch (err) {
      setMessages((m) => [
        ...m,
        { sender: "bot", text: "⚠️ Server not responding." },
      ]);
    }
  };

  return (
    <div className="flex flex-col h-[80vh] bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-4">
      <div className="flex-1 overflow-y-auto space-y-3 mb-3">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${
              msg.sender === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`max-w-[75%] px-4 py-2 rounded-2xl ${
                msg.sender === "user"
                  ? "bg-blue-600 text-white"
                  : "bg-gray-200 dark:bg-gray-700"
              }`}
            >
              {msg.text}
            </div>
          </div>
        ))}
      </div>

      <div className="flex items-center space-x-2 border-t border-gray-300 dark:border-gray-700 pt-2">
        <input
          type="text"
          placeholder="Type your symptoms..."
          className="flex-1 px-3 py-2 rounded-md bg-gray-100 dark:bg-gray-700 outline-none"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button
          onClick={sendMessage}
          className="bg-blue-600 text-white p-2 rounded-md hover:bg-blue-700"
        >
          <FaPaperPlane />
        </button>
      </div>
    </div>
  );
};

export default ChatPanel;
