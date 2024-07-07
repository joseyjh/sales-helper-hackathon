import { useEffect, useState } from 'react'
import { io } from 'socket.io-client'

const socket = io("http://localhost:8765");

export const ConnectingComponent = ({ addMessage }) => {
    const [ content, setContent ] = useState({ message: "", timestamp: "" });

    // interface MessageType {
    //     id: number;
    //     title: string;
    //     text: string;
    //   }
      
    function transformMessage(message): { id: number, title: string, text: string } {
        const newMessage = {
            id: Math.random(),
            text: message.message,
            title: ""
        }
        return newMessage
    }
    
    useEffect(() => {
        socket.on('connect', () => {
            console.log("Connected to WebSocket Server")
        });

        socket.on('message', (data) => {
            setContent(data);
            const newMessage = transformMessage(data)
            addMessage(newMessage)
        });

        socket.on('disconnect', () => {
            console.log("Disconnected from WebSocket Server")
        })
    }, []);

  return (
    <div>
    </div>
  )
}
