import requests

BASE_URL = "http://127.0.0.1:8000"

def lookup_user(phone_number):
    try:
        response = requests.post(
            f"{BASE_URL}/users/lookup",
            json={"phone_number": phone_number},
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        print(f"Error looking up user: {error}")
        return None

def register_user(phone_number, full_name, email, id_number):
    try:
        response = requests.post(
            f"{BASE_URL}/users/register",
            json={
                "phone_number": phone_number,
                "full_name": full_name,
                "email": email,
                "id_number": id_number,
            },
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as error:
        status_code = error.response.status_code

        if status_code == 409:
            return {
                "success": False,
                "message": "Phone number or ID number already registered."
            }

        if status_code == 422:
            return {
                "success": False,
                "message": "Invalid registration details. Please check your information."
            }

        return {
            "success": False,
            "message": "Registration failed. Please try again."
        }

    except requests.exceptions.RequestException:
        return None

def main():
    phone_number = input("Enter your phone number: ")

    result = lookup_user(phone_number)

    if result is None:
        print("Unable to connect to the registration service. Please try again later.")
        return

    if result["registered"]:
        print("Welcome back! You are already registered.")
    else:
        print("Welcome! Let's get you registered.")

        full_name = input("Enter your full name: ")
        email = input("Enter your email: ")
        id_number = input("Enter your ID number: ")

        result = register_user(
            phone_number,
            full_name,
            email,
            id_number
        )

        if result is None:
            print("Registration service unavailable. Please try again later.")
            return

        if result["success"]:
            print(result["message"])
        else:
            print(result["message"])


if __name__ == "__main__":
    main()


