import React, { useState } from 'react';
import './App.css';
import ReactMarkdown from 'react-markdown';
import rehypeHighlight from 'rehype-highlight';
import 'highlight.js/styles/github.css'; // or any other theme

function App() {
  const [input, setInput] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch('https://ai-dev-agent-backend.onrender.com/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: input }),
      });

      const data = await res.json();
      setResponse(data.response);
    } catch (error) {
      console.error("❌ Error fetching from backend:", error);
      setResponse("Failed to connect to backend.");
    }
  };

  return (
    <div className="App">
      <h1>AI Dev Agent Interface</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter a task or prompt..."
        />
        <button type="submit">Send</button>
      </form>
      <div className="response">
        <h2>Response:</h2>
      <ReactMarkdown rehypePlugins={[rehypeHighlight]}>
      {response}
      </ReactMarkdown>
      </div>
    </div>
  );
}

export default App;
