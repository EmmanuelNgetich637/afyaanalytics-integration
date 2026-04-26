import {
  createSession,
  initiateHandshake,
  completeHandshake
} from "./api.js";

import { startTokenTimer } from "./timer.js";

const logContainer = document.getElementById("logContainer");

let state = {
  session: null,
  handshake: null,
  tokens: null
};

function log(message, data = null) {
  const div = document.createElement("div");
  div.className = "log";
  div.innerText =
    message + (data ? "\n" + JSON.stringify(data, null, 2) : "");
  logContainer.prepend(div);
}

// --------------------
// INIT SESSION
// --------------------
document.getElementById("startBtn").addEventListener("click", async () => {
  document.getElementById("initStatus").innerText = "Creating session...";

  state.session = await createSession();

  log("SESSION CREATED", state.session);

  const res = await initiateHandshake();

  log("INIT RESPONSE", res);

  if (!res.success) {
    document.getElementById("initStatus").innerText = "Failed";
    return;
  }

  state.handshake = res.data;

  document.getElementById("handshakeToken").innerText =
    res.data.handshake_token;

  document.getElementById("initStatus").innerText = "Success";
});

// --------------------
// COMPLETE HANDSHAKE
// --------------------
document.getElementById("completeBtn").addEventListener("click", async () => {
  document.getElementById("completeStatus").innerText = "Completing...";

  const res = await completeHandshake();

  log("COMPLETE RESPONSE", res);

  if (!res.success) {
    document.getElementById("completeStatus").innerText = "Failed";
    return;
  }

  state.tokens = res.data;

  document.getElementById("accessToken").innerText =
    res.data.access_token;

  document.getElementById("refreshToken").innerText =
    res.data.refresh_token;

  document.getElementById("status").innerText = "Authenticated ✅";

  // ✅ START TOKEN TIMER (15 min)
  startTokenTimer(900);

  document.getElementById("completeStatus").innerText = "Success";
});

// --------------------
// COPY
// --------------------
window.copyToken = function (id) {
  const text = document.getElementById(id).innerText;
  navigator.clipboard.writeText(text);
};