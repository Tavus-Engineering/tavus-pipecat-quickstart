import React from 'react';
import VideoConversation from './components/VideoConversation';
import './App.css';
import tavusLogo from './assets/tavus_io_logo.jpeg';

function App() {
  return (
    <div className="app-container">
      {/* Header */}
      <header className="main-header">
        <div className="header-content">
          <div className="header-left">
            <div className="logo">
              <img src={tavusLogo} alt="Tavus" className="logo-image" />
              TAVUS
            </div>
            <nav className="main-nav">
              <a href="#" className="nav-link">DOCS</a>
              <a href="#" className="nav-link">PRICING</a>
              <a href="#" className="nav-link">ENTERPRISE</a>
              <a href="#" className="nav-link">CAREERS</a>
            </nav>
          </div>
          <div className="header-spacer"></div>
          <div className="header-right">
            <button className="btn-login">LOGIN</button>
            <button className="btn-get-started">GET STARTED</button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="hero-section">
        <h1 className="hero-title" style={{ letterSpacing: '-0.06em' }}>AI Humans, <br />at your service</h1>
        <p className="hero-subtitle" style={{ lineHeight: 1 }}>
          They're the best of both worlds: <br />the emotional intelligence of humanity,<br /> with the reach and reliability of machines.
        </p>
        <button className="btn-signup">SIGN UP FOR FREE</button>
      </section>

      {/* Video Component */}
      <VideoConversation />
    </div>
  );
}

export default App;