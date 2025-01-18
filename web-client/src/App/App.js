import React, { useState } from 'react';
import { useMediaQuery } from 'react-responsive';
import AppDesktop  from './AppDesktop';
import AppMobile from './AppMobile';

function App() {
  const isMobile = useMediaQuery({ maxWidth: 768 });
  const [fen, setFen] = useState('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1');

  return isMobile ? (
    <div className="mobile">
      <AppMobile 
        fen={fen} 
        setFen={setFen}
        isMobile={isMobile}
      />
    </div>
  ) : 
  (
    <div className="desktop">
      <AppDesktop 
        fen={fen} 
        setFen={setFen}
        isMobile={isMobile}
      />
    </div>
  );
}

export default App;