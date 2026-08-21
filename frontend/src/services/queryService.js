import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;

export const askQuery = async (query) => {
  const response = await axios.post(`${API_URL}/query`, {
    query,
  });

  return response.data;
};
