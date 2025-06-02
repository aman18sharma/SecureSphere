import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import VulnerabilityTable from './components/VulnerabilityTable';
import VulnerabilityDetail from './components/VulnerabilityDetail';
import VulnerabilityReport from './components/VulnerabilityReport';
import FileUploader from './components/FileUploader';
import './index.css';

function App() {
  return (
    <Router>
      <div className="app-container">
        <header>
          <h1>Vulnerability Management System</h1>
          <nav>
            <a href="/">Dashboard</a>
            <a href="/upload">Upload</a>
          </nav>
        </header>

        <main>
          <Routes>
            <Route path="/" element={<VulnerabilityTable />} />
            <Route path="/vulnerability/:id" element={<VulnerabilityDetail />} />
            <Route path='/vuln_assement_report/:id' element={<VulnerabilityReport/>} />
            <Route path="/upload" element={<FileUploader />} />
          </Routes>
        </main>

        <footer>
          <p>© 2025 Vulnerability Management System | AI-Powered Security</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;