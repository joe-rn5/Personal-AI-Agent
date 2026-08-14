const API_URL = "https://mats-blessed-determines-lbs.trycloudflare.com/chat";

const messages = [];
const chatLog = document.getElementById("chat-log");
const form = document.getElementById("chat-form");
const input = document.getElementById("chat-input");

function appendMessage(role, text) {
  const wrap = document.createElement("div");
  wrap.className = `msg msg-${role}`;

  const meta = document.createElement("div");
  meta.className = "msg__meta";
  const time = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  meta.textContent = `${role === "user" ? ">> you" : ">> agent"} · ${time}`;

  const body = document.createElement("div");
  body.className = "msg__text";
  body.textContent = text;

  wrap.append(meta, body);
  chatLog.appendChild(wrap);
  chatLog.scrollTop = chatLog.scrollHeight;
  return wrap;
}

function appendTyping() {
  const wrap = document.createElement("div");
  wrap.className = "msg msg-assistant msg-typing";
  wrap.innerHTML = `
    <div class="msg__meta">>> agent</div>
    <div class="msg__text"><span class="dots"><span>·</span><span>·</span><span>·</span></span></div>
  `;
  chatLog.appendChild(wrap);
  chatLog.scrollTop = chatLog.scrollHeight;
  return wrap;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const text = input.value.trim();
  if (!text) return;

  input.value = "";
  appendMessage("user", text);
  messages.push({ role: "user", content: text });

  const typingEl = appendTyping();

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages }),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    typingEl.remove();
    appendMessage("assistant", data.reply);
    messages.push({ role: "assistant", content: data.reply });
  } catch (err) {
    typingEl.remove();
    appendMessage("assistant", "Something went wrong reaching the agent — is the backend running?");
  }
});
