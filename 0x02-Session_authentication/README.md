# Session Authentication

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [API Routes](#api-routes)
  - [Login](#login)
  - [Logout](#logout)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [License](#license)
- [Contributing](#contributing)
- [Authors](#authors)

## Introduction
This project implements a session-based authentication system using Flask. The system allows users to log in and log out securely using session IDs stored in cookies, providing a convenient way to authenticate users without requiring them to enter their credentials repeatedly.

## Features
- **Session-based authentication**: Users authenticate using session IDs stored in cookies.
- **Secure login**: Passwords are validated securely.
- **Easy logout**: Users can log out, destroying the session.
- **API integration**: Simple APIs to handle login and logout actions.

## Requirements
- Python 3.7+
- Flask
- Werkzeug 0.12.1+
- Ubuntu 18.04 LTS
- Git

## Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your_username>/alx-backend-user-data.git
   cd alx-backend-user-data/0x02-Session_authentication
