serverResponseElement = document.getElementById('server_response')
document.getElementById("register_form_submit_button").addEventListener('click', async function(event) {
    
    event.preventDefault();
    
    const user_email = document.getElementById('register_form_email_input').value;
    const password = document.getElementById('register_form_password_input').value;

    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_email: user_email,
                password: password
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.json();
        serverResponseElement.innerText = JSON.stringify(result, null, 2);
        
        

    } catch (error) {
        console.error("Authentication failed:", error);
    }
});
