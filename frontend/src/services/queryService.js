import axios from "axios";

const API_URL = "http://localhost:8000";

export const askQuestion = async (question) => {
  const response = await axios.post(`${API_URL}/query`, {
    question,
  });

  return response.data;
};
