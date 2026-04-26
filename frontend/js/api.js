const BASE_URL = "http://127.0.0.1:5000";

let sessionId = null;

export async function createSession() {
  const res = await fetch(`${BASE_URL}/session/create`, {
    method: "POST"
  });

  const data = await res.json();
  sessionId = data.session_id;

  return sessionId;
}

export async function initiateHandshake() {
  const res = await fetch(`${BASE_URL}/session/${sessionId}/initiate`, {
    method: "POST"
  });

  return await res.json();
}

export async function completeHandshake() {
  const res = await fetch(`${BASE_URL}/session/${sessionId}/complete`, {
    method: "POST"
  });

  return await res.json();
}

export function getSessionId() {
  return sessionId;
}