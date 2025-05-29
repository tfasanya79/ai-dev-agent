import React, { useState } from 'react';
import './App.css';
import ReactMarkdown from 'react-markdown';
import rehypeHighlight from 'rehype-highlight';
import 'highlight.js/styles/github.css';

function App() {
  const [input, setInput] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

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
      console.error("❌ Error handling input:", error);
      setResponse("Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  const CodeBlock = ({ children }: { children: string[] }) => {
    const code = children[0];
    const [copied, setCopied] = useState(false);
    const [expanded, setExpanded] = useState(false);
    const isLong = code.split('\n').length > 10;

    const handleCopy = () => {
      navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 1000);
    };

    return (
      <div style={{ position: 'relative', marginBottom: '1rem', border: '1px solid #ddd', borderRadius: '6px' }}>
        <div style={{ padding: '0.5rem', backgroundColor: '#f9f9f9', borderBottom: '1px solid #eee' }}>
          <button onClick={handleCopy} style={{ marginRight: '8px' }}>
            {copied ? '✔ Copied' : 'Copy'}
          </button>
          {isLong && (
            <button onClick={() => setExpanded(!expanded)}>
              {expanded ? 'Collapse' : 'Expand'}
            </button>
          )}
        </div>
        <pre style={{ maxHeight: expanded || !isLong ? 'none' : '200px', overflowY: 'auto', margin: 0 }}>
          <code>{code}</code>
        </pre>
      </div>
    );
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
        <button type="submit" disabled={loading}>
          {loading ? 'Processing...' : 'Send'}
        </button>
      </form>
      <div className="response" style={{ maxHeight: '400px', overflowY: 'auto' }}>
        <h2>Response:</h2>
        <ReactMarkdown
          rehypePlugins={[rehypeHighlight]}
          components={{
            code: CodeBlock,
          }}
        >
          {response}
        </ReactMarkdown>
      </div>
    </div>
  );
}

export default App;
