let handshakeTimer = null;
let accessTimer = null;

function format(seconds) {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}:${s.toString().padStart(2, "0")}`;
}

/* --------------------------
   HANDSHAKE TIMER (900s)
-------------------------- */
export function startHandshakeTimer(seconds) {
  const el = document.getElementById("handshakeExpiry");

  clearInterval(handshakeTimer);

  let remaining = Number(seconds);

  if (isNaN(remaining)) remaining = 0;

  handshakeTimer = setInterval(() => {
    el.innerText = `Handshake expires in: ${format(remaining)}`;

    if (remaining <= 0) {
      clearInterval(handshakeTimer);
      el.innerText = "Handshake expired ❌";
      return;
    }

    remaining--;
  }, 1000);
}

/* --------------------------
   ACCESS TOKEN TIMER (21600s)
-------------------------- */
export function startAccessTimer(seconds) {
  const el = document.getElementById("tokenTimer");
  const status = document.getElementById("status");

  clearInterval(accessTimer);

  let remaining = Number(seconds);

  if (isNaN(remaining)) remaining = 0;

  accessTimer = setInterval(() => {
    el.innerText = `Time Remaining: ${format(remaining)}`;

    if (remaining <= 0) {
      clearInterval(accessTimer);

      el.innerText = "Token Expired ❌";

      status.innerText = "Session Expired ❌";
      status.style.color = "#ef4444";

      return;
    }

    remaining--;
  }, 1000);
}