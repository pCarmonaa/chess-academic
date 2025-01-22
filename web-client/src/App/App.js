import React, { useState } from 'react';
import { useMediaQuery } from 'react-responsive';
import { Helmet } from "react-helmet";
import AppDesktop  from './AppDesktop';
import AppMobile from './AppMobile';

function App() {
  const isMobile = useMediaQuery({ maxWidth: 768 });
  const [fen, setFen] = useState('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1');

  return (
    <>
      <Helmet>
        <script type="application/ld+json">
          {`
          {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "Chess Academic",
            "url": "https://chessacademic.com",
            "description": "Chess Academic is an AI-powered tool designed for analyzing chess positions. Use the interactive chessboard to set up positions and receive detailed strategic insights.",
            "keywords": "chess analysis, chess strategies, AI chess, chessboard positions, chess training, deep chess analysis, artificial intelligence chess tool"
          }
          `}
        </script>
        <title>Chess Academic - Deep Chess Analysis Powered by AI</title>
        <meta
          name="description"
          content="Chess Academic is an AI-powered tool designed for analyzing chess positions. Use the interactive chessboard to set up positions and receive detailed strategic insights."
        />
        <meta name="keywords" content="chess analysis, chess strategies, AI chess, chessboard positions, chess training, deep chess analysis, artificial intelligence chess tool" />
        <meta name="robots" content="index, follow" />
        <link rel="canonical" href="https://chessacademic.com" />
      </Helmet>
      {isMobile ? (
        <div className="mobile">
          <AppMobile fen={fen} setFen={setFen} isMobile={isMobile} />
        </div>
      ) : (
        <div className="desktop">
          <AppDesktop fen={fen} setFen={setFen} isMobile={isMobile} />
        </div>
      )}
    </>
  );
}

export default App;