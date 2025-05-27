def generate_frontend_code(spec: dict) -> dict:
    return {
        "frontend/package.json": """{
  "name": "frontend",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  },
  "devDependencies": {
    "vite": "^4.0.0"
  }
}""",

        "frontend/index.html": f"""<!DOCTYPE html>
<html lang="en">
  <head><meta charset="UTF-8"><title>{spec.get("title", "AI App")}</title></head>
  <body><div id="root"></div><script type="module" src="/src/main.jsx"></script></body>
</html>
""",

        "frontend/src/main.jsx": """import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode><App /></React.StrictMode>
);
""",

        "frontend/src/App.jsx": f"""import React from 'react';

function App() {{
  return (
    <div>
      <h1>Welcome to {spec.get("title", "your app")}</h1>
      <p>This app includes: {", ".join(spec.get("features", []))}</p>
    </div>
  );
}}

export default App;
""",
    }
