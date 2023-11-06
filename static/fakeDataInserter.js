async function insertFakeData() {
    const response = await fetch('/insert_fake_data');
    if (response.ok) {
        const data = await response.json();
        console.log(data)
        document.getElementById("username").value = data.username;
        document.getElementById("password").value = data.password;
        document.getElementById("first_name").value = data.first_name;
        document.getElementById("last_name").value = data.last_name;
        document.getElementById("address").value = data.address;
        document.getElementById("email").value = data.email;
        document.getElementById("phone").value = data.phone;
    } else {
        console.error('Failed to fetch fake data.');
    }
}