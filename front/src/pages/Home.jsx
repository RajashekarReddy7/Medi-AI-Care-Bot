// import React from 'react';

// function Home() {
//   return (
//     <div style={{
//       minHeight: '100vh',
//       background: 'linear-gradient(135deg, #0a1628 0%, #1a2332 50%, #0f1b2d 100%)',
//       color: 'white',
//       fontFamily: 'Georgia, serif',
//       position: 'relative',
//       overflow: 'hidden'
//     }}>
//       {/* Header */}
//       <header style={{
//         display: 'flex',
//         justifyContent: 'space-between',
//         alignItems: 'center',
//         padding: '2rem 3rem',
//         position: 'relative',
//         zIndex: 10
//       }}>
//         {/* Logo */}
//         <div style={{
//           display: 'flex',
//           alignItems: 'center',
//           gap: '0.5rem'
//         }}>
//           <div style={{
//             width: '50px',
//             height: '50px',
//             background: 'linear-gradient(135deg, #ec4899 0%, #8b5cf6 100%)',
//             borderRadius: '50%',
//             display: 'flex',
//             alignItems: 'center',
//             justifyContent: 'center',
//             fontSize: '28px'
//           }}>
//             ❤️
//           </div>
//           <span style={{
//             fontSize: '14px',
//             fontWeight: 'bold',
//             color: '#ec4899'
//           }}>CareBot AI</span>
//         </div>

//         {/* Buttons */}
//         <div style={{
//           display: 'flex',
//           gap: '1rem'
//         }}>
//           <button style={{
//             background: 'linear-gradient(135deg, #ec4899 0%, #f472b6 100%)',
//             color: 'white',
//             border: 'none',
//             padding: '0.75rem 2rem',
//             borderRadius: '25px',
//             fontSize: '16px',
//             fontWeight: '600',
//             cursor: 'pointer',
//             boxShadow: '0 4px 15px rgba(236, 72, 153, 0.4)',
//             transition: 'all 0.3s ease',
//             textTransform: 'uppercase',
//             letterSpacing: '1px'
//           }}
//           onMouseOver={(e) => {
//             e.target.style.transform = 'translateY(-2px)';
//             e.target.style.boxShadow = '0 6px 20px rgba(236, 72, 153, 0.6)';
//           }}
//           onMouseOut={(e) => {
//             e.target.style.transform = 'translateY(0)';
//             e.target.style.boxShadow = '0 4px 15px rgba(236, 72, 153, 0.4)';
//           }}>
//             LOGIN
//           </button>
//           <button style={{
//             background: 'linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%)',
//             color: 'white',
//             border: 'none',
//             padding: '0.75rem 2rem',
//             borderRadius: '25px',
//             fontSize: '16px',
//             fontWeight: '600',
//             cursor: 'pointer',
//             boxShadow: '0 4px 15px rgba(139, 92, 246, 0.4)',
//             transition: 'all 0.3s ease',
//             textTransform: 'uppercase',
//             letterSpacing: '1px'
//           }}
//           onMouseOver={(e) => {
//             e.target.style.transform = 'translateY(-2px)';
//             e.target.style.boxShadow = '0 6px 20px rgba(139, 92, 246, 0.6)';
//           }}
//           onMouseOut={(e) => {
//             e.target.style.transform = 'translateY(0)';
//             e.target.style.boxShadow = '0 4px 15px rgba(139, 92, 246, 0.4)';
//           }}>
//             SIGNUP
//           </button>
//         </div>
//       </header>

//       {/* Main Content */}
//       <div style={{
//         display: 'grid',
//         gridTemplateColumns: '1fr 1fr',
//         alignItems: 'center',
//         padding: '0 5rem',
//         maxWidth: '1400px',
//         margin: '0 auto',
//         minHeight: 'calc(100vh - 120px)'
//       }}>
//         {/* Left Side - Text Content */}
//         <div style={{
//           paddingRight: '3rem'
//         }}>
//           <h1 style={{
//             fontSize: '3.5rem',
//             fontWeight: 'normal',
//             marginBottom: '2rem',
//             lineHeight: '1.2',
//             background: 'linear-gradient(135deg, #ec4899 0%, #f472b6 100%)',
//             WebkitBackgroundClip: 'text',
//             WebkitTextFillColor: 'transparent',
//             backgroundClip: 'text'
//           }}>
//             Your Compassionate Health Guide
//           </h1>

//           <p style={{
//             fontSize: '1.25rem',
//             lineHeight: '1.8',
//             color: '#e2e8f0',
//             marginBottom: '2rem',
//             fontWeight: '300'
//           }}>
//             Experiencing symptoms? Worried about your health? Need quick guidance before seeing a doctor? CareBot is here for you.
//           </p>

//           <p style={{
//             fontSize: '1.1rem',
//             lineHeight: '1.8',
//             color: '#cbd5e1',
//             fontWeight: '300'
//           }}>
//             At <strong style={{ color: '#ec4899', fontWeight: '600' }}>TriageAI</strong>, we understand that timely and empathetic triage is a critical part of quality healthcare. Whether you're feeling unwell, uncertain, or simply need a quick assessment, our AI-driven triage assistant is here to guide you with compassion, accuracy, and respect for your well-being.
//           </p>
//         </div>

//         {/* Right Side - Illustration */}
//         <div style={{
//           display: 'flex',
//           justifyContent: 'center',
//           alignItems: 'center',
//           position: 'relative'
//         }}>
//           <div style={{
//             width: '500px',
//             height: '500px',
//             background: 'radial-gradient(circle, rgba(236, 72, 153, 0.15) 0%, transparent 70%)',
//             borderRadius: '50%',
//             position: 'absolute',
//             animation: 'pulse 3s ease-in-out infinite'
//           }}></div>
          
//           <div style={{
//             fontSize: '300px',
//             textAlign: 'center',
//             filter: 'drop-shadow(0 20px 40px rgba(236, 72, 153, 0.3))',
//             animation: 'float 6s ease-in-out infinite'
//           }}>
//             🌸
//           </div>
//         </div>
//       </div>

//       <style>{`
//         @keyframes pulse {
//           0%, 100% {
//             transform: scale(1);
//             opacity: 0.3;
//           }
//           50% {
//             transform: scale(1.1);
//             opacity: 0.2;
//           }
//         }

//         @keyframes float {
//           0%, 100% {
//             transform: translateY(0px);
//           }
//           50% {
//             transform: translateY(-20px);
//           }
//         }

//         @media (max-width: 1024px) {
//           div[style*="gridTemplateColumns"] {
//             grid-template-columns: 1fr !important;
//             padding: 0 2rem !important;
//           }
//         }
//       `}</style>
//     </div>
//   );
// }

// export default Home;
import React from "react";
import { useNavigate } from "react-router-dom";
import { Heart, Shield, Clock, Brain, LogIn } from "lucide-react";
import "../styles/HomePage.css";

function HomePage() {
  const navigate = useNavigate();

  return (
    <div className="homepage">
      {/* ===== HEADER ===== */}
      <header className="homepage-header">
        <div className="logo-container">
          <Heart className="logo-icon" />
          <h1 className="logo-text">Carebot</h1>
        </div>
        <div className="header-buttons">
          <button
            className="header-login-btn"
            onClick={() => navigate("/login")}
          >
            <LogIn size={16} /> Login
          </button>
          <button
            className="header-register-btn"
            onClick={() => navigate("/register")}
          >
            Register
          </button>
        </div>
      </header>

      {/* Spacer to prevent hero content from hiding behind navbar */}
      <div className="nav-spacer"></div>

      {/* ===== HERO SECTION ===== */}
      <section className="hero-section">
        <div className="hero-content">
          <h2 className="hero-title">Your AI Healthcare Assistant, 24/7</h2>
          <p className="hero-subtitle">
            Get instant medical guidance from our intelligent chatbot
          </p>
          <button className="cta-button" onClick={() => navigate("/chat")}>
            Start Conversation
          </button>
        </div>

        <div className="hero-image">
          <img
            src="https://cdni.iconscout.com/illustration/premium/thumb/doctor-consulting-patient-online-5594885-4660917.png"
            alt="Healthcare illustration"
          />
        </div>
      </section>

      {/* ===== FEATURES SECTION ===== */}
      <section className="features-section">
        <div className="feature-card">
          <Shield className="feature-icon" />
          <h3>Emergency Support</h3>
          <p>Quick response for urgent medical queries</p>
        </div>

        <div className="feature-card">
          <Clock className="feature-icon" />
          <h3>24/7 Availability</h3>
          <p>Healthcare guidance anytime you need</p>
        </div>

        <div className="feature-card">
          <Brain className="feature-icon" />
          <h3>AI-Powered</h3>
          <p>Smart diagnosis and health recommendations</p>
        </div>
      </section>

      {/* ===== FOOTER ===== */}
      <footer className="footer">
        © {new Date().getFullYear()} Carebot AI — Your Trusted Digital Health Assistant
      </footer>
    </div>
  );
}

export default HomePage;
