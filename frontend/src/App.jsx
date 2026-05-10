import { useState } from 'react';
import './App.css';

function App() {
  const [text, setText] = useState('');
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('text');

  const handleSummarize = async () => {
    setLoading(true);
    setError(null);
    setSummary('');

    try {
      const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      let response;

      if (activeTab === 'text') {
        if (!text.trim()) {
          throw new Error('Please enter some text to summarize.');
        }
        response = await fetch(`${BASE_URL}/summarize/text`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text, max_length: 150, min_length: 30 })
        });
      } else {
        if (!file) {
          throw new Error('Please upload a PDF file.');
        }
        const formData = new FormData();
        formData.append('file', file);
        formData.append('max_length', '150');
        formData.append('min_length', '30');

        response = await fetch(`${BASE_URL}/summarize/pdf`, {
          method: 'POST',
          body: formData
        });
      }

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Summarization failed.');
      }

      const data = await response.json();
      setSummary(data.summary);
      
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="hero-section">
        <h1 className="title">AI Summarizer</h1>
        <p className="subtitle">
          Instantly distill long documents into precise, actionable insights using advanced AI models.
        </p>
      </header>

      <main className="main-card">
        <div className="tabs-container">
          <button
            onClick={() => setActiveTab('text')}
            className={`tab-btn ${activeTab === 'text' ? 'active' : ''}`}
          >
            Text Input
          </button>
          <button
            onClick={() => setActiveTab('pdf')}
            className={`tab-btn ${activeTab === 'pdf' ? 'active' : ''}`}
          >
            PDF Upload
          </button>
        </div>

        <div className="input-wrapper">
          {activeTab === 'text' ? (
            <>
              <textarea
                className="text-area"
                placeholder="Paste your content here..."
                value={text}
                onChange={(e) => setText(e.target.value)}
              />
              <span className="char-count">{text.length} chars</span>
            </>
          ) : (
            <label className="upload-area">
              <input 
                type="file" 
                hidden 
                accept=".pdf" 
                onChange={(e) => setFile(e.target.files[0])} 
              />
              <svg className="upload-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
              <div className="upload-text">Click to upload or drag & drop</div>
              <div className="upload-subtext">PDF documents only</div>
              {file && (
                <div className="file-name">Selected: {file.name}</div>
              )}
            </label>
          )}
        </div>

        <button 
          className="action-btn" 
          onClick={handleSummarize} 
          disabled={loading}
        >
          {loading ? (
            <>
              <svg className="spinner" fill="none" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" style={{opacity: 0.25}} />
                <path fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" style={{opacity: 0.75}} />
              </svg>
              Processing...
            </>
          ) : (
            'Generate Summary ✨'
          )}
        </button>

        {error && (
          <div className="error-msg">
            {error}
          </div>
        )}

        {summary && (
          <div className="result-area">
            <h3 className="result-title">
              <svg className="result-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Summary Result
            </h3>
            <div className="summary-content">
              {summary}
            </div>
            <button 
              className="copy-btn"
              onClick={() => navigator.clipboard.writeText(summary)}
            >
              <svg className="copy-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              Copy to clipboard
            </button>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
