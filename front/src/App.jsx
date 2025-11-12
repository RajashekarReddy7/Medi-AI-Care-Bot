import { BrowserRouter, Routes, Route } from "react-router-dom";
import Chat from "./pages/Chat";
import Login from "./pages/Login";
import Home from "./pages/Home";
import SummaryView from "./pages/SummaryView";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/home" element={<Home />} />
        <Route path="/summary/:id" element={<SummaryView />} /> 
      </Routes>
    </BrowserRouter>
  );
}

export default App;
