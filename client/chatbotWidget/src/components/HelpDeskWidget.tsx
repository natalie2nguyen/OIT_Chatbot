import React, { useState } from 'react';
import { sendMessageToChatbot } from '../chatbotApi.ts';

// import app.css for styling/centering
import '../App.css'

const HelpDeskWidget: React.FC = () => {
  // State to hold the current message input by the user
  const [message, setMessage] = useState('');
  // // State to hold the history of chat messages
  const [chatHistory, setChatHistory] = useState<{ sender: string; text: string }[]>([]);

  // Function to handle message from input box
  const handlesSentMessage = async () => {
    if (message.trim()){
      try{
        // Appends user message
        setChatHistory((prevHistory: any) => [...prevHistory, { sender: 'You', text: message }]);

        const botResponse = await sendMessageToChatbot(message)

        // Appends bot response
        setChatHistory((prevHistory: any) => [...prevHistory, { sender: 'Bot', text: botResponse }]);

        setMessage('');
      }
      catch(error){
        console.error("Error sending message:" , error)
      }
      setMessage('');
    }
  }

  return(
    // Container div with some padding and iterating through chathistory for messages to display
    <div style={{padding: '10px'}}>
      <h1>ChatBox</h1>
      <div style={{ border: '1px solid #ccc', padding: '10px', height: '200px', overflowY: 'scroll' }}>
        {chatHistory.map((msg,index) => (
          <div key={index}>
            <strong>{msg.sender}:</strong>{msg.text}
          </div>
        ))}
      </div>

      <input
      type="text"
      value={message}
      onChange={(e) => setMessage(e.target.value)}
      placeholder="Write a message..."
      style={{marginTop: '10px', width: '80%'}}
      />
      
      <button onClick={handlesSentMessage} style={{marginTop: '10px'}}>
        Send
      </button>
    </div>
  );
};

export default HelpDeskWidget;