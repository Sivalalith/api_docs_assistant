import axios from "axios";

const API_URL = "http://localhost:8000";

export const askQuery = async (query) => {
  const response = await axios.post(`${API_URL}/query`, {
    query,
  });

  return response.data;
};
