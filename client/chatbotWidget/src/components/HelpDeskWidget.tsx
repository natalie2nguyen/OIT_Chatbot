// HelpDeskWidget.tsx

import React, { useEffect, useState } from 'react';
import { sendMessageToChatbot } from '../chatbotApi.ts';
import './HelpDeskWidget.css';

interface HelpDeskWidgetProps {
  onClose: () => void;
}

const HelpDeskWidget: React.FC<HelpDeskWidgetProps> = ({ onClose }) => {
  // States to hold the current message input by the user, history of chat messages, error, minimize state
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState<{ sender: string; text: string; timestamp: number }[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isMinimized, setIsMinimized] = useState(false);

  // Function to handle sending user message to the chatbot
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
    <div className='backgroundImage'>
      <div className="chat-widget-container">
      <div className="chat-widget-header">
        <h2>OIT ChatBot</h2>
        <div className="chat-widget-controls">
          <button onClick={() => setIsMinimized(!isMinimized)} className="minimize-button" aria-label="Minimize chat window">
            {isMinimized ? '▲' : '▼'}
          </button>
          <button onClick={onClose} className="close-button" aria-label="Close chat window">
            ✖
          </button>
        </div>
      </div>

      {!isMinimized && (
        <div className="chat-widget-body">
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
            <button onClick={handleSendMessage} className="button-style" aria-label="Send message">
              &#x27A4;
            </button>
          </div>
        </div>
      )}
    </div>
    </div>
    
  );
};

export default HelpDeskWidget;
