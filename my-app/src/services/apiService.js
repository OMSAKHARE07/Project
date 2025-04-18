const API_BASE_URL = 'http://localhost:8000'; // FastAPI backend URL

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error('File upload failed');
  }

  return response.json();
};

export const summarizeFile = async (filename) => {
  const response = await fetch(`${API_BASE_URL}/summarize/${filename}`, {
    method: 'GET',
  });

  if (!response.ok) {
    throw new Error('Summarization failed');
  }

  return response.json();
};

export const getSummaryResult = async () => {
  const response = await fetch(`${API_BASE_URL}/api/result`, {
    method: 'GET',
  });

  if (!response.ok) {
    throw new Error('Failed to fetch summary result');
  }

  return response.json();
}; 