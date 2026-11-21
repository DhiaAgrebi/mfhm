const ping_status_test_paragraph = document.getElementById( 'ping_status_test_paragraph' );
const ping_status_test_button = document.getElementById( 'ping_status_test_button' );


async function ping_server() {
    let response_to_ping = await fetch(/ping);
    ping_status_div_test_paragraph.innerText = response_to_ping;
}