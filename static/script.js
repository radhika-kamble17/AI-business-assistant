function showStatus(elementId, message, success = true) {
    const target = document.getElementById(elementId);
    if (!target) return;
    target.textContent = message;
    target.className = success ? "status-box success" : "status-box error";
    target.classList.remove("d-none");
}

function clearStatus(elementId) {
    const target = document.getElementById(elementId);
    if (!target) return;
    target.textContent = "";
    target.className = "status-box mt-3 d-none";
}

function appendChatBubble(role, text) {
    const chatWindow = document.getElementById("chatWindow");
    if (!chatWindow) return;

    const bubble = document.createElement("div");
    bubble.className = `chat-bubble ${role}`;

    const label = document.createElement("div");
    label.className = "chat-label";
    label.textContent = role === "user" ? "You" : "Assistant";

    const message = document.createElement("div");
    message.className = "bubble-content";
    message.textContent = text;

    bubble.appendChild(label);
    bubble.appendChild(message);
    chatWindow.appendChild(bubble);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

async function sendMessage(event) {
    if (event) event.preventDefault();

    const input = document.getElementById("userMessage");
    if (!input) return;

    const message = input.value.trim();
    if (!message) {
        showStatus("chatStatus", "Please type a question before sending.", false);
        return;
    }

    clearStatus("chatStatus");
    input.value = "";

    const chatForm = document.getElementById("chatForm");
    const submitButton = chatForm ? chatForm.querySelector("button[type='submit']") : null;
    if (submitButton) submitButton.disabled = true;

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message }),
        });

        const data = await response.json();
        const reply = data.reply || "No response received.";
        appendChatBubble("ai", reply);
    } catch (error) {
        appendChatBubble("ai", "Error connecting to AI assistant.");
        showStatus("chatStatus", "Error connecting to AI assistant.", false);
    } finally {
        if (submitButton) submitButton.disabled = false;
    }
}

async function submitLead(event) {
    if (event) event.preventDefault();

    const form = document.getElementById("leadForm");
    if (!form) return;

    const formData = new FormData(form);
    const payload = {
        name: formData.get("name") || "",
        email: formData.get("email") || "",
        phone: formData.get("phone") || "",
        course: formData.get("course") || "",
        message: formData.get("message") || "",
    };

    try {
        const response = await fetch("/submit_lead", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });

        const data = await response.json();
        document.getElementById("leadStatus").textContent = data.message || "Lead submitted successfully.";
        form.reset();
    } catch (error) {
        document.getElementById("leadStatus").textContent = "Lead submission failed.";
    }
}

async function deleteLead(leadId, rowElement) {
    if (!confirm("Delete this lead? This action cannot be undone.")) {
        return;
    }

    try {
        const response = await fetch("/delete_lead", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id: leadId }),
        });

        const data = await response.json();
        if (response.ok && data.success) {
            rowElement.remove();
        } else {
            alert(data.message || "Unable to delete lead.");
        }
    } catch (error) {
        alert("Unable to delete lead.");
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const chatForm = document.getElementById("chatForm");
    if (chatForm) {
        chatForm.addEventListener("submit", sendMessage);
    }

    const leadForm = document.getElementById("leadForm");
    if (leadForm) {
        leadForm.addEventListener("submit", submitLead);
    }

    document.addEventListener("click", function (event) {
        const deleteButton = event.target.closest(".delete-lead-button");
        if (!deleteButton) return;

        const leadId = deleteButton.getAttribute("data-lead-id");
        const row = deleteButton.closest("tr");
        if (leadId && row) {
            deleteLead(leadId, row);
        }
    });

    clearStatus("chatStatus");
});
