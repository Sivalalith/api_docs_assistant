import axios from "axios";

const API_URL = "http://localhost:8000";

export const uploadDocuments = async () => {
  const response = await axios.post(`${API_URL}/upload`);
  return response.data;
};
