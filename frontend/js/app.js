const btn = document.getElementById("startBtn");
const statusDiv = document.getElementById("status");
const resultDiv = document.getElementById("result");

btn.addEventListener("click", async () => {
  statusDiv.innerText = "⏳ Running handshake...";
  resultDiv.classList.add("hidden");

  try {
    const data = await startHandshake();

    console.log("API RESPONSE:", data); // 🔍 debug (keep this)

    if (!data.success) {
      statusDiv.innerText = "❌ Failed: " + data.message;
      return;
    }

    statusDiv.innerText = "✅ Handshake Successful";

    // ✅ IMPORTANT: correct path
    const tokens = data.data.data;

    if (!tokens) {
      statusDiv.innerText = "❌ No token data returned";
      return;
    }

    document.getElementById("accessToken").innerText =
      tokens.access_token || "N/A";

    document.getElementById("refreshToken").innerText =
      tokens.refresh_token || "N/A";

    document.getElementById("expiry").innerText =
      tokens.expires_at || "N/A";

    resultDiv.classList.remove("hidden");

  } catch (err) {
    console.error(err);
    statusDiv.innerText = "❌ Error: " + err.message;
  }
});