import {
  createSession,
  initiateHandshake,
  completeHandshake,
  refreshToken
} from "./api.js";

import {
  startHandshakeTimer,
  startAccessTimer
} from "./timer.js";

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

/* --------------------
   INIT SESSION
-------------------- */
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

  /* ✅ HANDSHAKE TIMER (900s) */
  startHandshakeTimer(res.data.expires_in_seconds);
});

/* --------------------
   AUTO REFRESH
-------------------- */
async function handleRefresh() {
  log("Refreshing token...");

  const res = await refreshToken(state.tokens.refresh_token);

  if (!res.success) {
    log("Refresh failed", res);
    return;
  }

  state.tokens = res.data;

  document.getElementById("accessToken").innerText =
    res.data.access_token;

  document.getElementById("refreshToken").innerText =
    res.data.refresh_token;

  log("Token refreshed", res.data);

  /* restart access timer */
  startAccessTimer(res.data.expires_in_seconds);
}

/* --------------------
   COMPLETE HANDSHAKE
-------------------- */
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
  document.getElementById("status").style.color = "#22c55e";

  /* ✅ ACCESS TOKEN TIMER (6h from backend) */
  startAccessTimer(res.data.expires_in_seconds);

  document.getElementById("completeStatus").innerText = "Success";
});

/* --------------------
   COPY
-------------------- */
window.copyToken = function (id) {
  const text = document.getElementById(id).innerText;
  navigator.clipboard.writeText(text);
};