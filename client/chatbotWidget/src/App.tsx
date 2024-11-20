// App.tsx

import React, { useState } from 'react';
import HelpDeskWidget from './components/HelpDeskWidget';
import './App.css';

function App() {
  const [isChatOpen, setIsChatOpen] = useState(false);

  return (
    <div className="App">
      {!isChatOpen && (
        <button className="chat-open-button" onClick={() => setIsChatOpen(true)} aria-label="Open chat window">
          💬
        </button>
      )}
      {isChatOpen && <HelpDeskWidget onClose={() => setIsChatOpen(false)} />}
    </div>
  );
}

export default App;
