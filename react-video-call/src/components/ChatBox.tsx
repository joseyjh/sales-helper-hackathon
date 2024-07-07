import React from 'react';
import { RxCross1 } from "react-icons/rx";

interface MessageType {
  id: number;
  title: string;
  text: string;
}

interface ChatBoxProps {
  initialMessage: string;
  messages: MessageType[];
  onStart: () => void; // Function to handle start event
  onStop: () => void; // Function to handle stop event
  startClicked: boolean; // Boolean to track if start button has been clicked
  onDelete: (id: number) => void; // Function to handle card deletion
  onInitialMessageDelete: () => void;
  className?: string; // Add className prop for additional styling
}



const ChatBox: React.FC<ChatBoxProps> = ({ initialMessage, messages, onStart, onStop, startClicked, onDelete, onInitialMessageDelete, className }) => {

  const handleButtonClick = () => {
    if (!startClicked) {
      onStart(); // Call the onStart function passed from App component
    } else {
      onStop(); // Call the onStop function passed from App component
    }
  };

  const handleDelete = (id: number) => {
    onDelete(id); // Call the onDelete function passed from App component
  };

  const handleInitialMessageDelete = () => {
    onInitialMessageDelete();
  };

  return (
    <div className={`ChatBox bg-blue-50 rounded-lg shadow-lg p-3 flex h-full w-full flex-col ${className}`}>
      <div className="flex-1 overflow-y-auto mb-4">
        {initialMessage && (
          <div className="p-4 mb-4 bg-gray-100 rounded-lg shadow-md transition-all duration-300 ease-in-out">
            <div className='relative'>
            <button
              onClick={handleInitialMessageDelete}
              className="absolute top-0 right-0 text-grey-700 hover:text-red-700"
            >
              <RxCross1 />
            </button>
            {initialMessage}
            </div>
          </div>
        )}
        {messages.map((message) => (
          <div key={message.id} className="relative">
            <button
              onClick={() => handleDelete(message.id)}
              className="absolute top-0 right-0 m-2 p-1 text-grey-700 hover:text-red-700"
            ><RxCross1 /></button>
            <div className="p-4 mb-4 bg-white rounded-lg shadow-md">
              <h2 className="font-bold">{message.title}</h2>
              <p style={{ overflowWrap: 'anywhere' }}>{message.text}</p>
            </div>
          </div>
        ))}
      </div>
      <div className="mt-auto border-t-2 border-gray-300 pt-1 flex justify-center">
        <button
          onClick={handleButtonClick}
          className={`${startClicked ? 'bg-red-500' : 'bg-green-500'} hover:${startClicked ? 'bg-red-700' : 'bg-green-700'} text-white font-bold py-2 px-16 rounded-full shadow-lg transition-all duration-300 ease-in-out`}
        >
          {startClicked ? "Stop" : "Start"}
        </button>
      </div>
    </div>
  );
};

export default ChatBox;
