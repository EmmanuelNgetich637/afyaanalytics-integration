const logContainer = document.getElementById("logContainer");

function log(message, data = null) {
  const div = document.createElement("div");
  div.className = "log";
  div.innerText = message + (data ? "\n" + JSON.stringify(data, null, 2) : "");
  logContainer.prepend(div);
}

// STEP 1
document.getElementById("startBtn").addEventListener("click", async () => {
  document.getElementById("initStatus").innerText = "Starting...";

  const res = await fetch("http://127.0.0.1:5000/start-handshake");
  const data = await res.json();

  log("INIT RESPONSE", data);

  if (!data.success) {
    document.getElementById("initStatus").innerText = "Failed";
    return;
  }

  document.getElementById("handshakeToken").innerText =
    data.data.data.access_token || "Token created";

  document.getElementById("initStatus").innerText = "Success";
});

// STEP 2
document.getElementById("completeBtn").addEventListener("click", async () => {
  document.getElementById("completeStatus").innerText = "Completing...";

  const res = await fetch("http://127.0.0.1:5000/start-handshake");
  const data = await res.json();

  log("COMPLETE RESPONSE", data);

  if (!data.success) {
    document.getElementById("completeStatus").innerText = "Failed";
    return;
  }

  const tokens = data.data.data;

  document.getElementById("accessToken").innerText = tokens.access_token;
  document.getElementById("refreshToken").innerText = tokens.refresh_token;
  document.getElementById("expiry").innerText = tokens.expires_at;

  document.getElementById("status").innerText = "Authenticated ✅";
});

// COPY
function copyToken(id) {
  const text = document.getElementById(id).innerText;
  navigator.clipboard.writeText(text);
  alert("Copied!");
}