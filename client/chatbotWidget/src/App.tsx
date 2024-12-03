// App.tsx

import React, { useState } from 'react';
import HelpDeskWidget from './components/HelpDeskWidget';
import './App.css';

function App() {
  const [isChatOpen, setIsChatOpen] = useState(false);

  return (
    <div className='backgroundImage'>
      <div className="App">
      {!isChatOpen && (
        <button className="chat-open-button" onClick={() => setIsChatOpen(true)} aria-label="Open chat window">
          
          <img src='/Chat_Icon.png'></img>
        </button>
      )}
      {isChatOpen && <HelpDeskWidget onClose={() => setIsChatOpen(false)} />}
    </div>
    </div>
    
  );
}

export default App;
