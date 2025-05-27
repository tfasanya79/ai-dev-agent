const form = document.getElementById("chat-form");
const input = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = input.value.trim();
  if (!message) return;

  // Show user message
  appendMessage("You", message, "user");

  // Clear input
  input.value = "";

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    const data = await response.json();
    appendMessage("AI", data.response, "ai");

  } catch (error) {
    console.error("Error:", error);
    appendMessage("AI", "Something went wrong...", "ai");
  }
});

function appendMessage(sender, text, role) {
  const div = document.createElement("div");
  div.classList.add("message", role);
  div.innerHTML = `<strong>${sender}:</strong> ${text}`;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}
