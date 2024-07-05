import { useEffect, useState } from 'react'
import { io } from 'socket.io-client'

const socket = io("http://localhost:8765");
export const ConnectingComponent = () => {
    const [ content, setContent ] = useState({ message: "", timestamp: "" });
    
    useEffect(() => {
        socket.on('connect', () => {
            console.log("Connected to WebSocket Server")
        });

        socket.on('message', (data) => {
            setContent(data);
        });

        socket.on('disconnect', () => {
            console.log("Disconnected from WebSocket Server")
        })
    }, []);

  return (
    <div style={{display: "flex", justifyContent: "center", alignItems: "center", fontSize: 50, height: "100vh", flexDirection: "column"}}>
        <h2 style={{display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center", height: "100%"}}>Websocket Client</h2>
        <h2 style={{display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center", height: "100%"}}>{content.timestamp}</h2>
        <h2 style={{display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center", height: "100%"}}>{content.message}</h2>
    </div>
  )
}
