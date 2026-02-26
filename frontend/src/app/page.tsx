"use client";

import Image from "next/image";
import { useState, useRef, useEffect } from "react";

// Mock types for messages
type Message = {
  id: string;
  sender: "user" | "bot";
  text: string;
};

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      sender: "user",
      text: "I was charged twice for the item i bought.",
    },
    {
      id: "2",
      sender: "bot",
      text: "**Brok:** Look runt, I didn't charge you twice, you likely clicked the button like a panicked mud-fly. \n\n**Sindri:** Oh dear! Please ignore my brother. Let me check the ledger right away to ensure we haven't made a terrible mistake. Could you provide your order number?",
    },
  ]);
  const [inputValue, setInputValue] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    // Add user message
    const newUserMessage: Message = {
      id: Date.now().toString(),
      sender: "user",
      text: inputValue,
    };
    setMessages((prev) => [...prev, newUserMessage]);
    setInputValue("");

    // --- Backend Integration Hook ---
    // Here is where you will call your FastAPI backend:
    // fetch('http://localhost:10000/chat', { ... })

    // For now, mock a bot response after a short delay
    setTimeout(() => {
      const mockBotMessage: Message = {
        id: (Date.now() + 1).toString(),
        sender: "bot",
        text: "**Brok:** I'm workin' on it, keep your beard on!\n\n**Sindri:** We are processing your request, please holding...",
      };
      setMessages((prev) => [...prev, mockBotMessage]);
    }, 1000);
  };

  // Helper function to render text with bold line breaks
  const formatMessageText = (text: string) => {
    return text.split("\n").map((line, i) => {
      // Basic markdown bold support for "**text**"
      const formattedLine = line.split(/(\*\*.*?\*\*)/).map((segment, j) => {
        if (segment.startsWith("**") && segment.endsWith("**")) {
          return <strong key={j} className="text-white">{segment.slice(2, -2)}</strong>;
        }
        return segment;
      });

      return (
        <span key={i}>
          {formattedLine}
          {i !== text.split("\n").length - 1 && <br />}
        </span>
      );
    });
  };

  return (
    <main className="relative w-full h-screen overflow-hidden bg-black font-sans text-gray-200">

      {/* --- LAYER 0: ENVIRONMENT --- */}
      <div className="absolute inset-0 -z-10">
        <Image
          src="/images/background.png"
          alt="Forge Background"
          fill
          className="object-cover object-center"
          priority
        />
        {/* Optional subtle overlay to ensure text contrast if needed */}
        <div className="absolute inset-0 bg-black/20" />
      </div>

      {/* --- LAYER 1: CHARACTERS --- */}
      {/* Brok (Left) */}
      <div className="absolute bottom-0 left-0 z-10 hidden md:block w-1/3 max-w-[450px] aspect-[3/4]">
        <Image
          src="/images/Brok_Render.png"
          alt="Brok"
          fill
          className="object-contain object-bottom drop-shadow-2xl"
          priority
        />
      </div>

      {/* Sindri (Right) */}
      <div className="absolute bottom-0 right-0 z-10 hidden md:block w-1/3 max-w-[450px] aspect-[3/4]">
        <Image
          src="/images/Sindri_profile.png"
          alt="Sindri"
          fill
          className="object-contain object-bottom drop-shadow-2xl"
          priority
        />
      </div>

      {/* --- LAYER 2: CHAT INTERFACE --- */}
      <div className="absolute inset-0 flex items-center justify-center z-20 pointer-events-none p-4 w-full">

        {/* Chat Container */}
        <div className="w-full max-w-2xl h-[75vh] flex flex-col bg-black/60 backdrop-blur-md border-2 border-amber-900/60 rounded-xl shadow-2xl overflow-hidden pointer-events-auto ring-1 ring-amber-500/20">

          {/* Header */}
          <div className="bg-[#2a1708]/90 border-b border-amber-900/60 px-6 py-4 flex items-center shadow-md">
            <h1 className="text-xl font-bold bg-gradient-to-r from-amber-200 to-amber-500 bg-clip-text text-transparent">
              Huldra Brothers Workshop
            </h1>
          </div>

          {/* Message History */}
          <div className="flex-1 overflow-y-auto p-6 space-y-6 custom-scrollbar">
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"
                  }`}
              >
                <div
                  className={`max-w-[85%] rounded-lg p-4 shadow-lg ${msg.sender === "user"
                    ? "bg-slate-800/80 border border-slate-600 shadow-slate-900/50 text-slate-200"
                    : "bg-[#3e2715]/80 border border-[#5c3a21] shadow-amber-950/50 text-amber-100/90"
                    }`}
                >
                  {/* Sender Name */}
                  <div
                    className={`text-xs mb-1 font-semibold ${msg.sender === "user" ? "text-slate-400" : "text-amber-500/80"
                      }`}
                  >
                    {msg.sender === "user" ? "User" : "Brok & Sindri Bot"}
                  </div>

                  {/* Message Content */}
                  <div className="leading-relaxed whitespace-pre-wrap">
                    {formatMessageText(msg.text)}
                  </div>
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="p-4 bg-black/80 border-t border-amber-900/60 backdrop-blur-lg">
            <form
              onSubmit={handleSendMessage}
              className="flex gap-3 focus-within:ring-1 focus-within:ring-amber-500/50 rounded-lg transition-all"
            >
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Type your message..."
                className="flex-1 bg-[#1a1a1a] border border-[#333] rounded-lg px-4 py-3 text-gray-200 placeholder-gray-500 focus:outline-none focus:border-amber-700 focus:bg-[#222] transition-colors"
                autoComplete="off"
              />
              <button
                type="submit"
                disabled={!inputValue.trim()}
                className="bg-amber-800 hover:bg-amber-700 disabled:opacity-50 disabled:cursor-not-allowed text-amber-100 font-semibold px-6 py-3 rounded-lg shadow-lg shadow-amber-900/20 transition-all border border-amber-700/50"
              >
                Send
              </button>
            </form>
          </div>

        </div>
      </div>
    </main>
  );
}
