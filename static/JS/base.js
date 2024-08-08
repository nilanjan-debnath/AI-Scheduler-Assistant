const url = new URL(window.location.href);
const statusValue = url.searchParams.get("status");
console.log(statusValue)