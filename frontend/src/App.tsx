import React, { useState } from 'react';
import './App.css';

interface ProjectMetadata {
  name: string;
  description: string;
}

function App() {
  const [step, setStep] = useState(0);
  const [input, setInput] = useState('');
  const [metadata, setMetadata] = useState<ProjectMetadata>({ name: '', description: '' });
  const [design, setDesign] = useState('');
  const [loading, setLoading] = useState(false);

  const handleNext = async () => {
    setLoading(true);
    if (step === 1) {
      // Save description and generate design
      const updatedMeta = { ...metadata, description: input };
      setMetadata(updatedMeta);
      await generateDesign(updatedMeta.name, updatedMeta.description);
      setStep(2);
    } else if (step === 2) {
      if (input.toLowerCase() === 'yes') {
        await startProject(metadata);
        setStep(3);
      } else {
        alert('You can upload your own design below.');
      }
    }
    setInput('');
    setLoading(false);
  };

  const generateDesign = async (name: string, description: string) => {
    try {
      const res = await fetch('http://127.0.0.1:8000/design', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, description }),
      });
      const data = await res.json();
      setDesign(data.system_design);
    } catch (err) {
      console.error('Design generation failed:', err);
      alert('Failed to generate design.');
    }
  };

  const handleUpload = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('project_name', metadata.name);

    try {
      const res = await fetch('http://127.0.0.1:8000/upload-design', {
        method: 'POST',
        body: formData,
      });

      const data = await res.json();
      alert(data.message || 'Design uploaded.');
      setStep(3);
    } catch (err) {
      console.error("Upload failed:", err);
      alert('Failed to upload file.');
    }
  };

  const startProject = async (meta: ProjectMetadata) => {
    try {
      const res = await fetch('http://127.0.0.1:8000/start-project', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(meta),
      });
      const data = await res.json();
      alert(data.message);
    } catch (err) {
      console.error('Failed to start project:', err);
      alert('Failed to start project.');
    }
  };

  const renderStep = () => {
    switch (step) {
      case 0:
        return (
          <>
            <h2>👋 Welcome to AI Dev Agent!</h2>
            <p>What is the name of your project?</p>
            <input value={input} onChange={(e) => setInput(e.target.value)} />
            <button onClick={() => {
              setMetadata((prev) => ({ ...prev, name: input }));
              setInput('');
              setStep(1);
            }}>Next</button>
          </>
        );
      case 1:
        return (
          <>
            <h2>📋 Describe your project</h2>
            <textarea value={input} onChange={(e) => setInput(e.target.value)} rows={4} />
            <button onClick={handleNext}>Generate Design</button>
          </>
        );
      case 2:
        return (
          <>
            <h2>🧠 Proposed System Design</h2>
            <pre style={{ whiteSpace: 'pre-wrap', backgroundColor: '#f0f0f0', padding: '1rem' }}>{design}</pre>
            <p>Do you accept this design?</p>
            <input
              type="text"
              placeholder="Type 'yes' or 'upload'"
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />
            {input.toLowerCase() === 'upload' && (
              <div>
                <input
                  type="file"
                  accept=".txt,.md"
                  onChange={(e) => {
                    const file = e.target.files?.[0];
                    if (file) handleUpload(file);
                  }}
                />
              </div>
            )}
            <button onClick={handleNext}>Confirm</button>
          </>
        );
      case 3:
        return <h2>✅ Project initialized and opened in VS Code!</h2>;
      default:
        return <p>🎉 You're done!</p>;
    }
  };

  return (
    <div className="App">
      <h1>AI Dev Agent</h1>
      {loading ? <p>⏳ Processing...</p> : renderStep()}
    </div>
  );
}

export default App;
