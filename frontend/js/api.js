const API_URL = "http://127.0.0.1:5000/start-handshake";

async function startHandshake() {
  const response = await fetch(API_URL);
  return await response.json();
}