import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;

export const getDocuments = async () => {
  const response = await axios.get(`${API_URL}/documents`);
  return response.data;
};

export const deleteDocument = async (id) => {
  const response = await axios.delete(`${API_URL}/documents/${id}`);
  return response.data;
};
