function scrollToBottom() {
  const chatContainer = document.getElementById("chatContainer");
  chatContainer.scrollTop = chatContainer.scrollHeight;
}
scrollToBottom();

function addLoading(text) {
  const user = document.getElementById("profile").innerText;
  const favicon = document.querySelector('link[rel="shortcut icon"]').getAttribute('href');
  const html = `<div class="chat">
        <div class="user chatText">
        <div class="uicon icon">${user}</div>
        <pre>${text}</pre>
        </div>
          <div class="ai chatText">
          <div class="aicon icon">
            <img src=${favicon} alt="ai" style="width: 1.5rem;">
          </div>
          <pre><div class="loader"></div></pre>
        </div>
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
