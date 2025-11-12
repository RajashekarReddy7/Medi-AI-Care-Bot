// import { useState } from "react";
// import { useNavigate } from "react-router-dom";
// import "../styles/login.css";

// export default function Login() {
//   const navigate = useNavigate();
//   const [isLogin, setIsLogin] = useState(true);
//   const [email, setEmail] = useState("");
//   const [password, setPassword] = useState("");

//   const toggleForm = () => setIsLogin(!isLogin);

//   const handleSubmit = async (e) => {
//     e.preventDefault();

//     if (!email || !password) {
//       alert("Please fill all fields");
//       return;
//     }

//     try {
//       if (isLogin) {
//         // 🔹 Login API
//         const formData = new URLSearchParams();
//         formData.append("username", email);
//         formData.append("password", password);

//         const res = await fetch("/login", {
//           method: "POST",
//           headers: { "Content-Type": "application/x-www-form-urlencoded" },
//           body: formData,
//         });

//         const data = await res.json();
//         if (data.access_token) {
//           localStorage.setItem("token", data.access_token);
//           navigate("/chat");
//         } else {
//           alert("Login failed");
//         }
//       } else {
//         // 🔹 Register API
//         const res = await fetch("/register", {
//           method: "POST",
//           headers: { "Content-Type": "application/json" },
//           body: JSON.stringify({ email, password }),
//         });

//         if (res.ok) {
//           alert("✅ Registered successfully. Please log in now.");
//           setIsLogin(true);
//         } else {
//           const err = await res.json();
//           alert("⚠️ " + (err.detail || "Registration failed"));
//         }
//       }
//     } catch (error) {
//       alert("❌ " + error.message);
//     }
//   };

//   return (
//     <div className="container">
//       {/* Left side info */}
//       <div className="info">
//         <h1>Welcome to AI CareBot</h1>
//         <p>
//           Your AI-powered healthcare assistant providing reliable, 24/7 support
//           for health queries.
//         </p>
//       </div>

//       {/* Right side login/register box */}
//       <div className="login-box">
//         <div className="logo">🩺</div>
//         <h2>{isLogin ? "Login" : "Register"}</h2>

//         <form
//           onSubmit={handleSubmit}
//           style={{ width: "100%", maxWidth: "320px" }}
//         >
//           <input
//             type="email"
//             placeholder="Email"
//             onChange={(e) => setEmail(e.target.value)}
//           />
//           <input
//             type="password"
//             placeholder="Password"
//             onChange={(e) => setPassword(e.target.value)}
//           />
//           <button type="submit">{isLogin ? "Login" : "Register"}</button>
//         </form>

//         <div className="toggle" onClick={toggleForm}>
//           {isLogin
//             ? "Don't have an account? Register"
//             : "Already have an account? Login"}
//         </div>
//       </div>
//     </div>
//   );
// }

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/login.css";
import { Eye, EyeOff, User, Lock } from "lucide-react";
import loginImage from "../assets/doctor.jpg"; // 👈 add a dummy image to /src/assets/

export default function Login() {
  const navigate = useNavigate();
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const toggleForm = () => setIsLogin(!isLogin);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!email || !password) {
      alert("Please fill all fields");
      return;
    }

    try {
      if (isLogin) {
        const formData = new URLSearchParams();
        formData.append("username", email);
        formData.append("password", password);

        const res = await fetch("/login", {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: formData,
        });

        const data = await res.json();
        if (data.access_token) {
          localStorage.setItem("token", data.access_token);
          navigate("/chat");
        } else {
          alert("Login failed");
        }
      } else {
        const res = await fetch("/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password }),
        });

        if (res.ok) {
          alert("✅ Registered successfully. Please log in now.");
          setIsLogin(true);
        } else {
          const err = await res.json();
          alert("⚠️ " + (err.detail || "Registration failed"));
        }
      }
    } catch (error) {
      alert("❌ " + error.message);
    }
  };

  return (
    <div className="auth-wrapper">
      {/* LEFT PANEL */}
      <div className="auth-left">
        <img src={loginImage} alt="Healthcare" />
      </div>

      {/* RIGHT PANEL */}
      <div className="auth-right">
        <div className="login-card">
          <div className="login-header">
            <div className="login-icon">🩺</div>
            <h2>{isLogin ? "Welcome Back" : "Create Account"}</h2>
            <p className="subtitle">
              {isLogin
                ? "Login to continue your healthcare journey"
                : "Start your AI healthcare journey today"}
            </p>
          </div>

          <form onSubmit={handleSubmit}>
            {!isLogin && (
              <div className="input-group">
                <User className="input-icon" />
                <input type="text" placeholder="Full name" required />
              </div>
            )}

            <div className="input-group">
              <User className="input-icon" />
              <input
                type="email"
                placeholder="Email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div className="input-group">
              <Lock className="input-icon" />
              <input
                type={showPassword ? "text" : "password"}
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <span
                className="eye-toggle"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <EyeOff /> : <Eye />}
              </span>
            </div>

            <button type="submit">{isLogin ? "Login" : "Create Account"}</button>
          </form>

          <p className="toggle" onClick={toggleForm}>
            {isLogin
              ? "Don’t have an account? Register here"
              : "Already have an account? Login here"}
          </p>
        </div>
      </div>
    </div>
  );
}
