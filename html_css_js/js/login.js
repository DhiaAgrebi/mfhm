const serverResponseElement = document.getElementById("server_response");
const loginSubmitButton = document.getElementById("login_form_submit_button");

loginSubmitButton.addEventListener("click", async (event) => {
  event.preventDefault();
  try {
    const response = await fetch("/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_email: document.getElementById("login_form_email_input").value,
        user_password: document.getElementById("login_form_password_input").value,
      }),
    });
    serverResponseElement.innerText = await response.text();
  } catch (err) {
    serverResponseElement.innerText = err.message;
  }
});