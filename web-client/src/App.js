import React, { useState } from 'react';
import './App.css';
import ChessboardComponent from './Chessboard/Chessboard';
import Chatbot from './Chatbot/Chatbot';
import logo from './logo.png';

function App() {
  const [fen, setFen] = useState('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1');

  return (
    <div className="App">
       <header className="App-header">
        <img src={logo} alt="Logo" className="App-logo" />
        <div>
          <h1>Chess Academic</h1>
          <h2 className="App-subtitle">Deep Chess Analysis Powered by Artificial Intelligence</h2>
        </div>
      </header>
      <main>
        <div className="container">
          <div className="chessboard-section">
            <ChessboardComponent fen={fen} setFen={setFen} />
          </div>
          <div className="chat-container">
            <Chatbot fen={fen} />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
