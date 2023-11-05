from typing import Optional, Dict

from .config import fake, user_data


def find_user(username: str, password: str) -> Optional[Dict[str, str]]:
    read_file()
    for user in user_data:
        if user["username"] == username and user["password"] == password:
            return user
    return None


def read_file() -> None:
    with open("user_data.txt", "r") as file:
        lines = file.readlines()

    for line in lines:
        data = line.strip().split(", ")
        user_dict = {}
        for item in data:
            key, value = item.split(": ")
            user_dict[key] = value
        user_data.append(user_dict)


def generate_fake_data() -> Dict[str, str]:
    fake_username = fake.user_name()
    fake_password = fake.password()
    fake_email = fake.email()
    fake_phone = fake.phone_number()
    return {
        "username": fake_username,
        "password": fake_password,
        "email": fake_email,
        "phone": fake_phone,
    }
