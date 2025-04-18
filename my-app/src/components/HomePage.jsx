import React, { useState } from 'react';
import './HomePage.css';
import { uploadFile, summarizeFile } from '../services/apiService';

const HomePage = () => {
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    e.preventDefault();
    const form = e.target;
    const fileInput = form.querySelector('input[type="file"]');
    const file = fileInput.files[0];

    if (!file) return alert('Please select a file.');

    setLoading(true);

    try {
      const uploadResult = await uploadFile(file);

      if (uploadResult.filename) {
        await summarizeFile(uploadResult.filename);
        window.location.href = '/result';
      } else {
        alert('Upload failed.');
      }
    } catch (err) {
      alert('Something went wrong: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <header>
        <h1>Validease</h1>
        <nav>
          <a href="#">Home</a>
          <a href="#upload">Upload</a>
          <a href="#features">Features</a>
          <a href="#about">About Us</a>
        </nav>
      </header>

      <section className="hero" id="upload">
        <h2>Validease</h2>
        <p>
          Empowering legal professionals and individuals by simplifying and summarizing legal documents with AI-powered precision.
        </p>

        {loading ? (
          <div className="loader">⏳ Processing... Please wait</div>
        ) : (
          <form onSubmit={handleUpload} className="upload-section" encType="multipart/form-data">
            <h3>Upload Your Document</h3>
            <input type="file" name="file" required />
            <button type="submit">Upload & Summarize</button>
          </form>
        )}
      </section>

      <section className="features" id="features">
        <h2>Features</h2>
        <div className="feature-list">
          <div className="feature-item">
            <h3>📝 Simplify Documents</h3>
            <p>Break down complex legal documents into understandable language.</p>
          </div>
          <div className="feature-item">
            <h3>🔍 Summarize Text</h3>
            <p>Extract key points and provide clear, concise summaries instantly.</p>
          </div>
          <div className="feature-item">
            <h3>⚡ AI-Powered Speed</h3>
            <p>Harness the power of advanced NLP to deliver results in seconds.</p>
          </div>
          <div className="feature-item">
            <h3>🔒 Secure Handling</h3>
            <p>Your documents are processed securely and never stored without consent.</p>
          </div>
        </div>
      </section>

      <section className="about" id="about">
        <h2>About Us</h2>
        <div className="team">
          <div className="member"><h4>Omkar Salgare</h4><p>Front-end Developer</p></div>
          <div className="member"><h4>Kushal Swamay</h4><p>Backend Developer</p></div>
          <div className="member"><h4>Shoiab Tamboli</h4><p>SEO Optimizer & System Developer</p></div>
          <div className="member"><h4>Omdatta Sakhare</h4><p>Backend Developer</p></div>
        </div>
      </section>

      <footer>&copy; 2025 Validease</footer>
    </>
  );
};

export default HomePage;
