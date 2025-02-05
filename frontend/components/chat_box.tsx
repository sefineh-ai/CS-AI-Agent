import React, { useState } from "react";
import { fetchChatResponse} from "../pages/api/chat"

const ChatBox = () => {
    const [messages, setMessages] = useState<{ text: string; type: "user" | "bot" }[]>([]);
    const [input, setInput] = useState("");

    const handleSend = async () => {
        if (!input) return;

        const newMessages = [...messages, { text: input, type: "user" }];
        setMessages(newMessages);
        setInput("");

        const response = await fetchChatResponse(input);
        setMessages([...newMessages, { text: response, type: "bot" }]);
    };

    return (
        <div>
            <div>
                {messages.map((msg, i) => (
                    <div key={i} className={msg.type === "user" ? "text-right" : "text-left"}>
                        {msg.text}
                    </div>
                ))}
            </div>
            <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Ask me anything..." />
            <button onClick={handleSend}>Send</button>
        </div>
    );
};

export default ChatBox;
