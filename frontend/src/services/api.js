const API_URL = "http://localhost:8000";

export const getVulnerabilities = async () => {
  const response = await fetch(`${API_URL}/vulnerabilities`);
  return response.json();
};

export const getVulnerability = async (id) => {
  const response = await fetch(`${API_URL}/vulnerabilities/${id}`);
  return response.json();
};

export const uploadVulnerabilities = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_URL}/upload`, {
    method: "POST",
    body: formData,
  });

  return response.json();
};

export const runAIAssessment = async (id) => {
  const response = await fetch(`${API_URL}/vulnerabilities/${id}/assess`, {
    method: "POST",
  });

  return response.json();
};

export const runOllamaAIAssessment = async (id) => {
  const response = await fetch(
    `${API_URL}/vulnerabilities/${id}/assess_by_ollama`,
    {
      method: "POST",
    }
  );

  return response.json();
};
