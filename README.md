# MAC Forgery Challenge

## Overview

This project implements a challenge to explore vulnerabilities in cryptographic Message Authentication Codes (MACs). Participants are tasked with forging a valid MAC for a given message. The challenge uses a Flask-based web application that provides two endpoints:

1. `/mac`: Generates a MAC for a provided message.
2. `/submit`: Allows submission of a forged MAC for validation.

---

## Setup and Execution

### Running Locally

Clone the repository and navigate to the project directory. 

```bash
docker compose up -d
```

### Docker

``` bash
docker pull vincent333/mac-ctf
docker run -d -t -p 5000:5000 --name mac-ctf vincent333/mac-ctf
```

---

## Endpoints

### `/mac` (POST)

Generates a MAC for the provided message.

#### Request Body
```json
{
    "message": "your_message_here"
}
```

#### Response
- **Success (200)**:
  ```json
  {
      "mac": ["r_hex", "t1_hex", ..., "td_hex"]
  }
  ```
- **Error (400)**:
  ```json
  {
      "error": "error_description"
  }
  ```

---

### `/submit` (POST)

Submits a forged MAC for validation. The goal is to construct a valid MAC for a message not previously queried.

#### Request Body
```json
{
    "mac": ["r_hex", "t1_hex", ..., "td_hex"],
    "message": "your_message_here"
}
```

#### Response
- **Success (200)**:
  ```json
  {
      "result": "Success! Here is your flag: FLAG{XXX}"
  }
  ```
- **Failure (400)**:
  ```json
  {
      "error": "error_description"
  }
  ```
- **Failure (200)**:
  ```json
  {
      "result": "Invalid MAC. Try again."
  }
  ```

---

### `/` (GET)

Provides instructions for the challenge in HTML format.

---
