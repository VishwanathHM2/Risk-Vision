import axios from "axios";

const BASE_URL = "http://localhost:8000";

export function fetchPrices(payload) {
  return axios.post(`${BASE_URL}/api/prices`, payload)
    .then((res) => res.data);
}

export function analyze(payload) {
  return axios.post(`${BASE_URL}/api/analyze`, payload)
    .then((res) => res.data);
}
