import axios from "axios";

const API_URL = "http://localhost:8000";

export const getDocuments = async () => {
  const response = await axios.get(`${API_URL}/documents`);
  return response.data;
};

export const deleteDocument = async (id) => {
  const response = await axios.delete(`${API_URL}/documents/${id}`);
  return response.data;
};
