async function insertFakeData() {
    const response = await fetch('/insert_fake_data');
    if (response.ok) {
        const data = await response.json();
        document.getElementById("username").value = data.username;
        document.getElementById("password").value = data.password;
        document.getElementById("email").value = data.email;
        document.getElementById("phone").value = data.phone;
    } else {
        console.error('Failed to fetch fake data.');
    }
}