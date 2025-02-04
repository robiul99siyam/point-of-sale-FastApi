![Image](https://github.com/user-attachments/assets/795630db-6322-40d1-a2ad-91bd61a0ecfc)
# 🔐 Point of Sales Server API Routes

## Getting started

Install All the packages

```bash or cmd
pip install "fastapi[standard]"
```

Start JSON server (with _JSON server Auth_ as middleware) :

```bash
fastapi dev main.py
```

# 📁 Collection: Auth

## End-point: Registration

### Register User

This endpoint is used to register a new user.

#### Request Body

- username (text, required): The username of the user.
- password (text, required): The password for the user account.
- role (text, required): The user role  of the user.
- image (image, required): The image of the user.

### Method: POST

> ```
> {{BASE_URL}}/api/user
> ```

### Body (**raw**)

```json
 {
    "username": "string",
    "password": "string",
    "role": "admin",
    "image": "string"
  }
```

⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

## End-point: Login

### Auth Login

This endpoint is used to authenticate a user and obtain a token for accessing protected resources.

#### Request Body

- username (text, required): The username of the user.
- password (text, required): The password of the user.

#### Response

- Status: 200 OK
- Content-Type: application/json
- user (object): Contains the user details including id, first name, last name, avatar, and email.
  - id (string): The unique identifier of the user.
  - username (string): The  username of the user.
  - password (string): The password of the user.
  - image (string): The image of the user.
  - role (string): The role of the user.
- token (object): Contains the authentication token and refresh token.
  - token (string): The authentication token.
  - bearer type (string)

### Method: POST

> ```
> {{BASE_URL}}/login
> ```

### Body (**raw**)

```json
{
  "username": "odoo",
  "password": "odoo"
}
```


# update here
