const login = document.getElementById("log")
const logForm = document.getElementById("logForm")
const register = document.getElementById("reg")
const regForm = document.getElementById("regForm")

login.addEventListener('click', () => {
    register.classList.remove("highlight");
    login.classList.add("highlight");
    regForm.classList.add("hide");
    logForm.classList.remove("hide");
});

register.addEventListener('click', () => {
    login.classList.remove("highlight");
    register.classList.add("highlight");
    logForm.classList.add("hide");
    regForm.classList.remove("hide");
});