import React, { useState } from 'react';
import { sendMessageToChatbot } from '../chatbotApi.ts';

// imports for styling/centering
import '../HelpDeskWidget.css'
import '../App.css'

const HelpDeskWidget: React.FC = () => {
  // States to hold the current message input by the user, history of chat messages and client facing error
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState<{ sender: string; text: string , timestamp: number}[]>([]);
  const [error, setError] = useState<string | null>(null);

  // Function to handle sending usermessage to the chatbot
  const handleSendMessage = async () => {
    if (message){
      try{
        // Trims and stores the users message
        const UserMessage = message.trim()

        // Timestamp for the users message
        const userTimestamp = Date.now()

        // Updates users message to the history
        setChatHistory(prevHistory => [...prevHistory, { sender: 'You', text: UserMessage, timestamp: userTimestamp}]);

        // Send message and await for a response from the server
        const botResponse = await sendMessageToChatbot(UserMessage)

        // Timestamp for bots incoming message and update bot 
        const botTimestamp = Date.now()
        setChatHistory(prevHistory => [...prevHistory, { sender: 'Bot', text: botResponse, timestamp: botTimestamp }]);
      }
      catch(error){
        // Logging error and display for users on frontend 
        console.error("Error sending message:" , error)
        setError('Failed to send message. Please try again.');

        // Clear error message after 3 seconds
        setTimeout(() => {setError(null)}, 3000); //
      }
      
      // Clearing out the messages to allow for new input
      setMessage('');
      
    }
  }

  return(
    // Container div with some padding and iterating through chathistory by timestamp to display
    <div style={{padding: '10px'}}>
      <h1>ChatBox</h1>
        {/* Client side error notification */}
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}
      <div style={{ border: '1px solid #ccc', padding: '10px', height: '200px', overflowY: 'scroll' }}>
        {chatHistory.map((msg) => (
          <div key={msg.timestamp} className="message">
            <div>
              <strong>{msg.sender}:</strong>{msg.text}
            </div>
            <div className="timestamp">
              {new Date(msg.timestamp).toLocaleTimeString()}
            </div>
          </div>
        ))}
      </div>

      {/* Input box for the message and allows for enter to trigger function call */}
      <input
      type="text"
      value={message}
      onChange={(e) => setMessage(e.target.value)}
      onKeyPress={(e) => {
        if (e.key === 'Enter') {
          e.preventDefault();
          handleSendMessage();
        }
      }}
      placeholder="Write a message..."
      className="input-style"
      />
      
      {/* Button tied with onclick in order to trigger function call */}
      <button onClick={handleSendMessage} className="button-style">
        Send
      </button>
    </div>
  );
};

export default HelpDeskWidget;
