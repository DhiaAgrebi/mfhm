document.getElementById('register_form').addEventListener('submit', async function(event) {
    
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
        console.log("Server response:", result);
        

    } catch (error) {
        console.error("Authentication failed:", error);
    }
});
