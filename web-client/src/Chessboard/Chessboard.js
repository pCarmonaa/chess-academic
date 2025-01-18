import React, { useState, useEffect, useRef } from 'react';
import { Chess } from 'chess.js';
import ChessboardDesktop from './ChessboardDesktop';
import ChessboardMobile from  './ChessboardMobile';

const ChessboardComponent = ({ fen, setFen, isMobile }) => {

  const [game, setGame] = useState(new Chess(fen));
  const [pgn, setPgn] = useState(game.pgn());
  const [history, setHistory] = useState([]);
  const [orientation, setOrientation] = useState('white');
  const [selectedSquares, setSelectedSquares] = useState([]);
  const [stockfishSquares, setStockfishScuares] = useState([]);
  const [isStockfishEnabled, setIsStockfishEnabled] = useState(false);
  const [bestMove, setBestMove] = useState(null);
  const [bestLines, setBestLines] = useState(isMobile ? [''] : ['', '', '']);
  const [score, setScore] = useState('');
  const stockfishDepth = process.env.REACT_APP_STOCKFISH_DEPTH || 18;
  const [boardWidth, setBoardWidth] = useState(isMobile ? window.innerWidth * 0.85 : window.innerWidth * 0.35);
  const [adjustedHeight, setAdjustedHeight] = useState(window.innerHeight * 0.1);

  const stockfishRef = useRef(null);

  const pieceSymbols = {
    K: '♔',
    Q: '♕',
    R: '♖',
    B: '♗',
    N: '♘',
  };

  const updateBoardWidth = () => {
    if(isMobile) {
      setBoardWidth(window.innerWidth * 0.85);
    }
    else {
      setBoardWidth(window.innerWidth * 0.35);
    }
  };
  const updateAdjustedHeight = () => {
    setAdjustedHeight(window.innerHeight * 0.1);
  };
  
  const onDrop = (sourceSquare, targetSquare, piece) => {
    try {
      var promotion = piece[1].toLowerCase();
      const move = game.move({
        from: sourceSquare,
        to: targetSquare,
        promotion: promotion,
      });

      if (move === null) 
        return false;

      setFen(game.fen());
      setPgn(game.pgn({ max_width: 5, newline_char: ' ' }));
      setHistory(game.history());
      analyzePosition(game.fen());
      return true;
    } 
    catch {
      return false;
    }
  };

  const handleFenChange = (event) => {
    const currentFen = game.fen();
    try {
      const newFen = event.target.value;
      setFen(newFen);
      const newGame = new Chess(newFen);
      setGame(newGame);
      setPgn(newGame.pgn({ max_width: 5, newline_char: ' ' }));
      setHistory(newGame.history());
      analyzePosition(game.fen());
    }
    catch {
      setFen(currentFen);
    }
  };

  const handlePgnChange = (event) => {
    const newPgn = event.target.value;
    const standardizedPgn = replaceEmoticonsWithText(newPgn);
    setPgn(newPgn);
  
    try {
      const newGame = new Chess();
      newGame.loadPgn(standardizedPgn);
      setGame(newGame);
      setFen(newGame.fen());
      setHistory(newGame.history());
      analyzePosition(game.fen());
    } catch {
      console.error("PGN inválido");
    }
  };
  
  const convertToEmoticonsText = (pgnLine) => {
    if (typeof pgnLine !== 'string') return '';
    return pgnLine
      .split('')
      .map((char) => (pieceSymbols[char] ? pieceSymbols[char] : char))
      .join('');
  };

  const replaceEmoticonsWithText = (pgn) => {
    const emoticonToText = {
      '♔': 'K',
      '♕': 'Q',
      '♖': 'R',
      '♗': 'B',
      '♘': 'N'
    };
  
    return pgn
      .split('')
      .map((char) => (emoticonToText[char] !== undefined ? emoticonToText[char] : char))
      .join('');
  };

  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.key === 'ArrowLeft') {
        goBack();
      } else if (event.key === 'ArrowRight') {
        goForward();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  });

  useEffect(() => {
    window.addEventListener('resize', updateBoardWidth);
    return () => {
      window.removeEventListener('resize', updateBoardWidth);
    };
  }, []);
  useEffect(() => {
    window.addEventListener('resize', updateAdjustedHeight);
    return () => {
      window.removeEventListener('resize', updateAdjustedHeight);
    };
  }, []);

  const goBack = () => {
    game.undo();
    setFen(game.fen());
    setPgn(game.pgn({ max_width: 5, newline_char: ' ' }));
    analyzePosition(game.fen());
  };

  const goForward = () => {
    const moves = game.history({ verbose: true });
    const nextMove = history[moves.length];
    if (nextMove) {
      game.move(nextMove);
      setFen(game.fen());
      setPgn(game.pgn({ max_width: 5, newline_char: ' ' }));
      analyzePosition(game.fen());
    }
  };

  const handleRightClick = (square) => {
    setSelectedSquares((prevSelectedSquares) => {
      if (prevSelectedSquares.includes(square)) {
        return prevSelectedSquares.filter((s) => s !== square);
      } else {
        return [...prevSelectedSquares, square];
      }
    });
  };

  const handleLeftClick = () => {
    setSelectedSquares([]);
  };

  const flipBoard = () => {
    setOrientation(orientation === 'white' ? 'black' : 'white');
  };

  const resetBoard = () => {
    const newGame = new Chess();
 
    setGame(newGame);
    setFen(newGame.fen());
    setPgn(newGame.pgn());
    setHistory([]);
    setSelectedSquares([]);
    setStockfishScuares([]);
    setBestMove(null);
    setBestLines(isMobile ? [''] : ['', '', '']);
    setScore('');
  };

  const customSquareStyles = [...selectedSquares, ...stockfishSquares].reduce((acc, square) => {
    if (selectedSquares.includes(square)) {
      acc[square] = {
        backgroundColor: 'rgba(240, 99, 92, 0.5)',
        boxShadow: '0 0 10px rgba(240, 99, 92, 0.9)',
      };
    }
  
    if (stockfishSquares.includes(square)) {
      acc[square] = {
        backgroundColor: 'rgba(255, 255, 102, 0.5)',
        boxShadow: '0 0 10px rgba(255, 255, 102, 0.9)',
      };
    }
  
    return acc;
  }, {});

  useEffect(() => {
    stockfishRef.current = new Worker('/stockfish.js');
  
    stockfishRef.current.onmessage = (event) => {
      const message = event.data;
  
      if (typeof message === 'string') {
        if (message.startsWith('bestmove')) {
          handleBestMove(message);
        } else if (message.startsWith('info depth')) {
          handleInfoDepth(message);
        }
      }
    };
  
    return () => stockfishRef.current?.terminate();
  }, [game]);
  
  const handleBestMove = (message) => {
    const move = message.split(' ')[1];
    setBestMove(move);
  };
  
  const handleInfoDepth = (message) => {
    handlePvLine(message);
    handleScore(message);
  };
  
  const handlePvLine = (message) => {
    const match = message.match(/\bpv \b(.+)/);
    if (match) {
      const pv = match[1];
      const pgn = convertPvToPgn(game.fen(), pv);
  
      setBestLines((prev) => {
        const updated = [...prev, pgn];
        return isMobile ? updated.slice(-1) : updated.slice(-3);
      });
    }
  };
  
  const handleScore = (message) => {
    const scoreMatch = message.match(/score (cp|mate) (-?\d+)/);
    if (scoreMatch) {
      const type = scoreMatch[1];
      let value = parseInt(scoreMatch[2], 10);
  
      const turn = game.fen().split(' ')[1];
      if (turn === 'b' && type === 'cp') {
        value *= -1;
      }
      setScore(type === 'cp' ? `${value / 100}` : `#${value}`);
    }
  };
  

  useEffect(() => {
    if (isStockfishEnabled && game) {
      analyzePosition(game.fen());
    }
    else {
          setBestMove(null);
          setBestLines(isMobile ? [''] : ['', '', '']);
          setScore('');
          setStockfishScuares([]);
    }
  }, [game, isStockfishEnabled]);

  const convertPvToPgn = (fen, pv) => {
    const chess = initializeChess(fen);
    const moves = extractMoves(pv);
    applyMoves(chess, moves);
    const fullPgn = generateFullPgn(chess);
    const pgnLine = filterPgnHeader(fullPgn);
    return convertToEmoticons(pgnLine);
  };
  
  const initializeChess = (fen) => new Chess(fen);
  
  const extractMoves = (pv) => pv.split(' ');
  
  const applyMoves = (chess, moves) => {
    moves.forEach((move) => chess.move(move));
  };
  
  const generateFullPgn = (chess) => chess.pgn({ max_width: 5, newline_char: ' ' });
  
  const filterPgnHeader = (fullPgn) => {
    const lines = fullPgn.split('\n').filter((line) => !line.startsWith('['));
    return lines.join(' ');
  };
  
  const convertToEmoticons = (pgnLine) => {
    if (typeof pgnLine !== 'string') return '';
      
    return pgnLine.split('').map((char, index) => {
      if (pieceSymbols[char]) {
        return (
          <span key={index} className="chess-symbol">
            {pieceSymbols[char]}
          </span>
        );
      }
      return <span key={index}>{char}</span>;
    });
  };

  const analyzePosition = (fen) => {
    if (isStockfishEnabled && stockfishRef.current) {
      stockfishRef.current.postMessage(`position fen ${fen}`);
      stockfishRef.current.postMessage(`go depth ${stockfishDepth}`);
    }
  };

  const toggleStockfish = () => {
    setIsStockfishEnabled((prev) => !prev);
  };

  const highlightBestMove = () => {
    if (bestMove) {
      const from = bestMove.slice(0, 2);
      const to = bestMove.slice(2, 4);
      setStockfishScuares([from, to]);
    }
  };

  useEffect(() => {
    highlightBestMove();
  }, [bestMove]);

  return isMobile ? (
    <div className="mobile">
      <ChessboardMobile
        fen={fen} 
        onDrop={onDrop} 
        boardWidth={boardWidth} 
        orientation={orientation} 
        resetBoard={resetBoard} 
        flipBoard={flipBoard} 
        score={score} 
        pgn={pgn} 
        bestLines={bestLines} 
        customSquareStyles={customSquareStyles} 
        adjustedHeight={adjustedHeight} 
        isStockfishEnabled={isStockfishEnabled} 
        toggleStockfish={toggleStockfish} 
        convertToEmoticonsText={convertToEmoticonsText} 
        handleRightClick={handleRightClick} 
        handleLeftClick={handleLeftClick} 
        handleFenChange={handleFenChange} 
        goBack={goBack} 
        goForward={goForward}
        handlePgnChange={handlePgnChange}
      />
    </div>
  ) : 
  (
    <div className="desktop">
      <ChessboardDesktop
        fen={fen} 
        onDrop={onDrop} 
        boardWidth={boardWidth} 
        orientation={orientation} 
        resetBoard={resetBoard} 
        flipBoard={flipBoard} 
        score={score} 
        pgn={pgn} 
        bestLines={bestLines} 
        customSquareStyles={customSquareStyles} 
        adjustedHeight={adjustedHeight} 
        isStockfishEnabled={isStockfishEnabled} 
        toggleStockfish={toggleStockfish} 
        convertToEmoticonsText={convertToEmoticonsText} 
        handleRightClick={handleRightClick} 
        handleLeftClick={handleLeftClick} 
        handleFenChange={handleFenChange} 
        goBack={goBack} 
        goForward={goForward}
        handlePgnChange={handlePgnChange}
      />
    </div>
  );
};

export default ChessboardComponent;