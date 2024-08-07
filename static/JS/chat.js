function scrollToBottom() {
  const chatContainer = document.getElementById("chatContainer");
  chatContainer.scrollTop = chatContainer.scrollHeight;
}
scrollToBottom();

function addLoading(text) {
  const html = `<div class="chat">
        <div class="user chatText"><pre>${text}</pre></div>
        <div class="ai chatText"><pre><div class="loader"></div></pre></div>
    </div>`;
  document.getElementById("chatContainer").innerHTML += html;
  scrollToBottom();
}

function handleTextarea() {
  const textarea = document.querySelector("#text_input");
  const data = textarea.value;
  addLoading(data);
  textarea.value = "";
}

document.getElementById("myForm").addEventListener("submit", function (event) {
  event.preventDefault();
  const formData = new FormData(this);
  handleTextarea();
  const url = "/input";
  fetch(url, {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      location.reload();
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});
