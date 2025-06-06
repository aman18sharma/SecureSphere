import React, { useState } from 'react';
import { uploadVulnerabilities } from '../services/api';

const FileUploader = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file');
      return;
    }

    setUploading(true);
    setError('');
    setMessage('');

    try {
      const result = await uploadVulnerabilities(file);
      console.log(result)
      setMessage(result.message);
    } catch (err) {
      setError('Failed to upload file. Please check the format.');
      console.error('Upload error:', err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="file-uploader">
      <h2>Upload Vulnerability JSON</h2>
      <form onSubmit={handleSubmit}>
        <div className="file-input">
          <input
            type="file"
            accept=".json"
            onChange={handleFileChange}
            disabled={uploading}
          />
        </div>

        <button
          type="submit"
          disabled={uploading || !file}
          className="upload-button"
        >
          {uploading ? 'Uploading...' : 'Upload Vulnerabilities'}
        </button>
      </form>

      {message && <div className="success-message">{message}</div>}
      {error && <div className="error-message">{error}</div>}

      <div className="format-info">
        <h4>Expected JSON Format:</h4>
        <pre>
          {`[
  {
    "title": "SQL Injection",
    "description": "Vulnerability allows SQL injection...",
    "severity": "High",
    "cve_id": "CVE-2023-12345"
  },
  ...
]`}
        </pre>
      </div>
    </div>
  );
};

export default FileUploader;