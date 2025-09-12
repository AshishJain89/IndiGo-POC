import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Send, Bot, User, Sparkles, X } from "lucide-react";

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatAssistantProps {
  onClose?: () => void;
}

const PROVIDERS = [
  { label: "Groq", value: "groq" },
  { label: "Perplexity", value: "perplexity" },
  { label: "OpenAI", value: "openai" },
  { label: "Cursor", value: "cursor" },
];

async function sendMessageToBackend(message: string, history: {role: string, content: string}[], provider: string): Promise<string> {
  try {
    const response = await fetch("/api/chat/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message, history, provider }),
    });
    if (!response.ok) {
      throw new Error("Failed to get response from backend");
    }
    const data = await response.json();
    return data.response || "No response from backend.";
  } catch (error) {
    return `Error: ${error instanceof Error ? error.message : "Unknown error"}`;
  }
}

export function ChatAssistant({ onClose }: ChatAssistantProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      type: "assistant",
      content:
        "Hello! I'm your Crew Rostering AI Assistant. I can help you regenerate rosters, check compliance, analyze disruptions, and answer questions about crew scheduling.",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [provider, setProvider] = useState("groq");

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: "user",
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    // Prepare history for backend (exclude timestamps and ids)
    const history = [...messages, userMessage].map((msg) => ({
      role: msg.type === "user" ? "user" : "assistant",
      content: msg.content,
    }));

    // Call backend API
    const aiResponse = await sendMessageToBackend(userMessage.content, history.slice(0, -1), provider);
    const aiMessage: Message = {
      id: (Date.now() + 1).toString(),
      type: "assistant",
      content: aiResponse,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, aiMessage]);
    setLoading(false);
  };

  return (
    <Card className="h-full flex flex-col shadow-lg">
      <CardHeader className="border-b border-border pb-4">
        <CardTitle className="flex items-center gap-2">
          <Bot className="h-5 w-5 text-primary" />
          AI Assistant
          <Badge variant="secondary" className="ml-auto">
            <Sparkles className="h-3 w-3 mr-1" />
            Online
          </Badge>
          {onClose && (
            <Button variant="ghost" size="sm" onClick={onClose} className="ml-2 h-6 w-6 p-0">
              <X className="h-4 w-4" />
            </Button>
          )}
        </CardTitle>
        <div className="mt-2 flex gap-2 items-center">
          <span className="text-xs text-muted-foreground">Provider:</span>
          <select
            className="border rounded px-2 py-1 text-xs"
            value={provider}
            onChange={(e) => setProvider(e.target.value)}
            disabled={loading}
          >
            {PROVIDERS.map((p) => (
              <option key={p.value} value={p.value}>{p.label}</option>
            ))}
          </select>
        </div>
      </CardHeader>
      
      <CardContent className="flex-1 flex flex-col p-4">
        <ScrollArea className="flex-1 pr-4">
          <div className="space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex items-start gap-3 ${
                  message.type === "user" ? "flex-row-reverse" : ""
                }`}
              >
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center ${
                    message.type === "user" 
                      ? "bg-primary text-primary-foreground" 
                      : "bg-muted text-muted-foreground"
                  }`}
                >
                  {message.type === "user" ? (
                    <User className="h-4 w-4" />
                  ) : (
                    <Bot className="h-4 w-4" />
                  )}
                </div>
                <div
                  className={`rounded-lg p-3 max-w-[80%] ${
                    message.type === "user"
                      ? "bg-primary text-primary-foreground"
                      : "bg-muted text-muted-foreground"
                  }`}
                >
                  <p className="text-sm">{message.content}</p>
                  <p className="text-xs opacity-70 mt-1">
                    {message.timestamp.toLocaleTimeString()}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </ScrollArea>
        
        <div className="flex gap-2 pt-4 border-t border-border">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask me about crew scheduling..."
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            className="flex-1"
            disabled={loading}
          />
          <Button onClick={handleSend} size="icon" disabled={loading}>
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}