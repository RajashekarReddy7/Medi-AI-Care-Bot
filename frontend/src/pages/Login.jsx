import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    const data = new URLSearchParams();
    data.append("username", email);
    data.append("password", password);

    const res = await fetch("http://127.0.0.1:8000/login", {
      method: "POST",
      body: data,
    });

    if (res.ok) {
      const { access_token } = await res.json();
      localStorage.setItem("token", access_token);
      navigate("/chat");
    } else {
      alert("Invalid credentials");
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <h2>Login</h2>
      <input type="email" placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
      <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} />
      <button type="submit">Login</button>
      <p onClick={() => navigate("/register")}>Register</p>
    </form>
  );
}

export default Login;
