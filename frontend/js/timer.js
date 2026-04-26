let timerInterval = null;

export function startTokenTimer(durationSeconds = 900) {
  const display = document.getElementById("tokenTimer");
  const expiryEl = document.getElementById("expiry");
  const statusEl = document.getElementById("status");

  let remaining = durationSeconds;

  if (timerInterval) {
    clearInterval(timerInterval);
  }

  if (statusEl) {
    statusEl.innerText = "Authenticated ✅ (Active Session)";
    statusEl.style.color = "#22c55e";
  }

  function update() {
    const minutes = Math.floor(remaining / 60);
    const seconds = remaining % 60;

    const formatted = `${minutes}:${seconds.toString().padStart(2, "0")}`;

    if (display) {
      display.innerText = `Time Remaining: ${formatted}`;
    }

    if (expiryEl) {
      expiryEl.innerText = `Expires in: ${formatted}`;
    }

    if (remaining <= 0) {
      clearInterval(timerInterval);

      if (display) display.innerText = "Token Expired ❌";

      if (statusEl) {
        statusEl.innerText = "Session Expired ❌";
        statusEl.style.color = "#ef4444";
      }

      return;
    }

    remaining--;
  }

  update();
  timerInterval = setInterval(update, 1000);
}

export function stopTokenTimer() {
  if (timerInterval) {
    clearInterval(timerInterval);
  }
}