import React, { useEffect, useState } from 'react';
import { sendMessageToChatbot } from '../chatbotApi.ts';

// imports for styling/centering
import './HelpDeskWidget.css'
import '../App.css'

const HelpDeskWidget: React.FC = () => {
  // States to hold the current message input by the user, history of chat messages and client facing error
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState<{ sender: string; text: string , timestamp: number}[]>([]);
  const [error, setError] = useState<string | null>(null);

  // Function to handle sending usermessage to the chatbot
  const handleSendMessage = async () => {
    if (message) {
      try {
        const UserMessage = message.trim();
        const userTimestamp = Date.now();
  
        // Create a local copy of the chat history including the user's message
        let newChatHistory = [
          ...chatHistory,
          { sender: 'You', text: UserMessage, timestamp: userTimestamp },
        ];
  
        // Update the state immediately with the user's message
        setChatHistory(newChatHistory);
  
        // Send message and await response
        const botResponse = await sendMessageToChatbot(UserMessage);
        const botTimestamp = Date.now();
  
        // Add the bot's response to the local chat history
        newChatHistory = [
          ...newChatHistory,
          { sender: 'Bot', text: botResponse, timestamp: botTimestamp },
        ];
  
        // Update the state with the new chat history including bot's message
        setChatHistory(newChatHistory);
      } catch (error) {
        console.error('Error sending message:', error);
        setError('Failed to send message. Please try again.');
  
        // Clear error message after 3 seconds
        setTimeout(() => {
          setError(null);
        }, 3000);
      } finally {
        // Clear the input field
        setMessage('');
      }
      
      
    }
  };

  const messageEndRef = React.useRef<HTMLDivElement>(null);

  useEffect(() => {
    messageEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory]);

  return (
    <div style={{ padding: '10px' }}>
      <h1>OIT ChatBot</h1>
      {/* Client side error notification */}
      {error && <div className="error-message">{error}</div>}
  
      <div className="chatbox">
        {chatHistory.map((msg) => (
          <div
            key={msg.timestamp}
            className={`message-container ${
              msg.sender === 'You' ? 'you' : 'bot'
            }`}
          >
            <div className={`bubble ${msg.sender === 'You' ? 'you' : 'bot'}`}>
              {msg.text}
              <div className="timestamp">
                {new Date(msg.timestamp).toLocaleTimeString()}
              </div>
            </div>
          </div>
        ))}
        <div ref={messageEndRef} />
      </div>
  
      {/* Input box for the message and allows for enter to trigger function call */}
      <div className="input-container">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyUp={(e) => {
            if (e.key === 'Enter') {
              handleSendMessage();
            }
          }}
          placeholder="Write a message..."
          className="input-style"
        />
        <button onClick={handleSendMessage} className="button-style">
          &#x27A4; {/* Unicode character for the arrow */}
        </button>
      </div>
    </div>
  );
};

export default HelpDeskWidget;
