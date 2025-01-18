import React from 'react';
import { Chessboard as ReactChessboard } from 'react-chessboard';
import { FaArrowLeft, FaArrowRight, FaSyncAlt, FaUndo } from 'react-icons/fa';
import './Chessboard.css';

const ChessboardMobile = (props) => {
  const {
    fen,
    onDrop,
    boardWidth,
    orientation,
    resetBoard,
    flipBoard,
    score,
    pgn,
    bestLines,
    customSquareStyles,
    adjustedHeight,
    isStockfishEnabled,
    toggleStockfish,
    convertToEmoticonsText,
    handleRightClick,
    handleLeftClick,
    handleFenChange,
    goBack,
    goForward,
    handlePgnChange
  } = props;

  const stopSwipePropagation = (e) => {
    if(e.target.closest(".react-chessboard")) {
      e.stopPropagation();
    }
  };

  return (
    <div 
      className="chessboard-wrapper" 
      onPointerDown={stopSwipePropagation}
    >
      <div className="chessboard-container">
        <ReactChessboard
          position={fen}
          onPieceDrop={onDrop}
          boardWidth={boardWidth}
          boardOrientation={orientation}
          customSquareStyles={customSquareStyles}
          onSquareRightClick={handleRightClick}
          onSquareClick={handleLeftClick}
        />
        <div className="controls">
          <button className="reset-button" onClick={resetBoard}>
            <FaUndo />
          </button>
          <button className="flip-button" onClick={flipBoard}>
            <FaSyncAlt />
          </button>
          <div className="navigation-buttons">
            <button onClick={goBack}>
              <FaArrowLeft />
            </button>
            <button onClick={goForward}>
              <FaArrowRight />
            </button>
          </div>
        </div>
      </div>
      <div className="info-container">
        <div className="stockfish-control">
          <h2 className="stockfish-title">Stockfish v16 NNUE</h2>
          <div className="container">
            <label class="stockfish-toggle">
              <input
                type="checkbox"
                checked={isStockfishEnabled}
                onChange={toggleStockfish}
              />
              <span class="slider"></span>
            </label>
            <span class="score-display-text">{score || '---'}</span>
          </div>
          <div className="best-lines">
            {bestLines.map((line, index) => (
              <div key={index} className="pgn-line" style={{ height: adjustedHeight }}>
                {line}
              </div>
            ))}
          </div>
        </div> 
        <div className="fen-pgn-container">
          <div className="fen-input">
            <label htmlFor="fen">FEN</label>
            <textarea id="fen" value={fen} onChange={handleFenChange} />
          </div>
          <div className="pgn-input">
            <label htmlFor="pgn">PGN</label>
            <textarea
              id="pgn"
              value={convertToEmoticonsText(pgn)}
              onChange={handlePgnChange}
              placeholder="Set a valid PGN"
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default ChessboardMobile;