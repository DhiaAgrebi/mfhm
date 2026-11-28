serverResponseElement = document.getElementById('server_response')
buttonClicked = document.getElementById('button_clicked')
document.getElementById("login_form_submit_button").addEventListener('click', async function(event) {
    
    event.preventDefault();
    
    const user_email = document.getElementById('login_form_email_input').value;
    const user_password = document.getElementById('login_form_password_input').value;

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_email: user_email,
                user_password: user_password
            })
        });

        if (!response.ok) {
            buttonClicked.innerText = response.status;
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        buttonClicked.innerText = "button clicked";
        const result = await response.json();
        buttonClicked.innerText = "response awaited";
        
        

    } catch (error) {
        console.error("Authentication failed:", error);
    }
});
