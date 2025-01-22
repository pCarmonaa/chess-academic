import React, { useState } from "react";
import './App.css';
import ChessboardComponent from '../Chessboard/Chessboard';
import Chatbot from '../Chatbot/Chatbot';
import logo from '../logo.png';
import { useSwipeable } from "react-swipeable";

const AppMobile = (props) => {
  const { fen, setFen, isMobile } = props;
  const [tabIndex, setTabIndex] = useState(0);

  const handlers = useSwipeable({
    onSwipedLeft: (eventData) => {
      if(!eventData.event.target.closest(".chessboard-container")) {
        setTabIndex((prevIndex) => (prevIndex === 0 ? 1 : 0));
      }
    },
    onSwipedRight: (eventData) => {
      if(!eventData.event.target.closest(".chessboard-container")) {
        setTabIndex((prevIndex) => (prevIndex === 1 ? 0 : 1));
      }
    },
    trackMouse: true,
  });

  const handleTabClick = (index) => {
    setTabIndex(index);
  };

  return (
    <div className="App" {...handlers}>
      <header className="App-header">
        <div className="header-title-row">
          <img src={logo} alt="Chess Academic Logo" className="App-logo" />
          <div className="title-container">
            <h1>Chess Academic</h1>
            <h2 className="App-subtitle">Deep Chess Analysis Powered by AI</h2>
          </div>
        </div>
      </header>
      <div className="tabs">
        <button
          className={`tab-button ${tabIndex === 0 ? "active" : ""}`}
          onClick={() => handleTabClick(0)}
        >
          Chess board
        </button>
        <button
          className={`tab-button ${tabIndex === 1 ? "active" : ""}`}
          onClick={() => handleTabClick(1)}
        >
          Chat bot
        </button>
      </div>
      <div className="tab-content">
        <div className={`chessboard-section ${tabIndex === 0 ? "active-tab" : "hidden-tab"}`} >
          <ChessboardComponent fen={fen} setFen={setFen} isMobile={isMobile} />
        </div>
        <div className={`chat-container ${tabIndex === 1 ? "active-tab" : "hidden-tab"}`} >
          <Chatbot fen={fen} />
        </div>
      </div>
    </div>
  );
};

export default AppMobile;