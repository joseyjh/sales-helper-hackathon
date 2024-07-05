import React, { useState } from 'react';
import ChatBox from './components/ChatBox';
import VideoCall from './components/VideoCall';
import { ConnectingComponent } from './components/ConnectingComponent';


// Define MessageType
interface MessageType {
  id: number;
  title: string;
  text: string;
}

const App: React.FC = () => {
  const [messages, setMessages] = useState<MessageType[]>([]);
  const [startClicked, setStartClicked] = useState(false);
  const [initialMessage, setInitialMessage] = useState<string>("");

  const handleStart = () => {
    if (!startClicked) {
      // Logic to send initial message
      setInitialMessage("Hello! I am your bot.");
      setStartClicked(true); // Set start clicked to true

      setTimeout(() => {
        setInitialMessage("");
      }, 5000);
    }
  };

  const handleStop = () => {
    // Logic to stop chat or handle stop event
    setStartClicked(false); // Set start clicked to false
    //setMessages([]); // Optionally clear messages when stopped
    //setInitialMessage("");
  };

  const handleDeleteMessage = (id: number) => {
    setMessages(messages.filter(message => message.id !== id));
  };

  const handleInitialMessageDelete = () => {
    setInitialMessage(""); // Clear initial message
  };

  const addMessage = (newMessage: MessageType) => {
    setMessages(prevMessages => {
      const updatedMessages = [...prevMessages, newMessage];
      return updatedMessages.length > 5 ? updatedMessages.slice(-5) : updatedMessages;
    });
  };


  return (
    <div className="App h-screen bg-black flex flex-col justify-center items-center">
      <div className="grid grid-cols-4 w-full h-full">
        <div className="col-span-3 bg-blue-100 flex justify-center items-center">
          <div className="w-full h-full flex items-center justify-center">
            <VideoCall />
            <ConnectingComponent />
          </div>
        </div>
        <div className="col-span-1 bg-white p-2 flex flex-col items-center shadow-lg h-full">
          <h1 className="text-3xl font-bold mb-2 border-b-2">Bot Insights</h1>
          <ChatBox initialMessage={initialMessage} messages={messages} onStart={handleStart} onStop={handleStop} startClicked={startClicked} onDelete={handleDeleteMessage}  onInitialMessageDelete={handleInitialMessageDelete}/>
        </div>
      </div>
    </div>
  );
};

export default App
