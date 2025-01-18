import React from 'react';
import { Chessboard as ReactChessboard } from 'react-chessboard';
import { FaArrowLeft, FaArrowRight, FaSyncAlt, FaUndo } from 'react-icons/fa';
import './Chessboard.css';

const ChessboardDesktop = (props) => {
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

  return (
    <div className="chessboard-wrapper">
      <div className="info-container">
        <div className="stockfish-control">
          <h2 className="stockfish-title">Stockfish v16 NNUE</h2>
          <div className="stockfish-toggle">
            <label className="switch">
              <input
                type="checkbox"
                checked={isStockfishEnabled}
                onChange={toggleStockfish}
              />
              <span className="slider round"></span>
            </label>
            <span className="score-display-text">
              {score || '---'}
            </span>
          </div>
          <div className="best-lines">
            {bestLines.map((line, index) => (
              <div key={index} className="pgn-line" style={{ height: adjustedHeight }}>
                {line}
              </div>
            ))}
          </div>
        </div>
        <div className="fen-input">
          <label htmlFor="fen">FEN</label>
          <textarea id="fen" value={fen} onChange={handleFenChange} style={{ height: adjustedHeight*0.8 }}/>
        </div>
        <div className="pgn-input">
          <label htmlFor="pgn">PGN</label>
          <textarea
            id="pgn"
            value={convertToEmoticonsText(pgn)}
            onChange={handlePgnChange}
            placeholder="Set a valid PGN"
            style={{ height: adjustedHeight*2 }}
          />
        </div>
      </div>
      <div className="chessboard-container">
        <button className="reset-button" onClick={resetBoard}>
          <FaUndo />
        </button>
        <button className="flip-button" onClick={flipBoard}>
          <FaSyncAlt />
        </button>
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
          <div className="navigation-buttons">
            <button onClick={goBack}>
              <FaArrowLeft />
            </button>
            <button onClick={goForward}>
              < FaArrowRight />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ChessboardDesktop;