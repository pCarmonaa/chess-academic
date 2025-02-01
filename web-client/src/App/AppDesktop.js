import React from 'react';
import './App.css';
import ChessboardComponent from '../Chessboard/Chessboard';
import Chatbot from '../Chatbot/Chatbot';
import logo from '../logo.png';

const AppDesktop = (props) => {
  const {
    fen,
    setFen,
    isMobile
  } = props;
  
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} alt="Intelli Chess Lab Logo" className="App-logo" />
        <div>
          <h1>Intelli Chess Lab</h1>
          <h2 className="App-subtitle">Deep Chess Analysis Powered by Artificial Intelligence</h2>
        </div>
      </header>
      <main>
        <div className="container">
          <div className="chessboard-section">
            <ChessboardComponent fen={fen} setFen={setFen} isMobile={isMobile} />
          </div>
          <div className="chat-container">
            <Chatbot fen={fen} />
          </div>
        </div>
      </main>
    </div>
  );
}
  
export default AppDesktop;