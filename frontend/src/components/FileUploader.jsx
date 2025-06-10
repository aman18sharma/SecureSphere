import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { uploadVulnerabilities, runOllamaAIAssessment } from "../services/api";

const FileUploader = () => {
  const navigate = useNavigate(); // ✅ Move hook to the top level
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [fileContent, setFileContent] = useState("");

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);

    if (selectedFile) {
      const reader = new FileReader();
      reader.onload = (event) => {
        try {
          const jsonContent = JSON.parse(event.target.result);
          setFileContent(JSON.stringify(jsonContent, null, 2)); // Format JSON with indentation
        } catch (err) {
          setError("Invalid JSON format");
          setFileContent("");
        }
      };
      reader.readAsText(selectedFile);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      setError("Please select a file");
      return;
    }

    setUploading(true);
    setError("");
    setMessage("");

    try {
      const result = await uploadVulnerabilities(file);
      console.log(result);
      setMessage(result?.message + " Ollama Llama3 assessment in progress.");

      if (result?.message?.toLowerCase().includes("vulnerability already exists")) {
        console.log("Vulnerability already exists");
        navigate(`/vulnerability/${result?.ids[0]}`);
      } else {
        // runOllamaAIAssessment(result?.ids[0]);
      }
    } catch (err) {
      setError("Failed to upload file. Please check the format.");
      console.error("Upload error:", err);
    } finally {
      setUploading(false);
    }
  }
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
          {uploading ? "Uploading..." : "Upload Vulnerabilities"}
        </button>
      </form>

      {message && <div className="success-message">{message}</div>}
      {error && <div className="error-message">{error}</div>}

      {fileContent && (
        <div className="json-preview">
          <h4>Preview:</h4>
          <pre>{fileContent}</pre>
        </div>
      )}
    </div>
  );
};

export default FileUploader;
