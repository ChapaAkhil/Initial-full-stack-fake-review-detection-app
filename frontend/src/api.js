import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const analyzeUrl = async (productUrl) => {
  const response = await axios.post(`${API_URL}/analyze-url`, {
    product_url: productUrl,
  });
  return response.data;
};

export const analyzeReviews = async (reviews) => {
  const response = await axios.post(`${API_URL}/analyze-reviews`, {
    reviews,
  });
  return response.data;
};
