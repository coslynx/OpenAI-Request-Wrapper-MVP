<div class="hero-icon" align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" />
</div>

<h1 align="center">
OpenAI-Request-Wrapper-MVP
</h1>
<h4 align="center">A Python Backend Application for Simplifying OpenAI API Interactions</h4>
<h4 align="center">Developed with the software and tools below.</h4>
<div class="badges" align="center">
  <img src="https://img.shields.io/badge/Language-Python-blue" alt="Programming Language: Python">
  <img src="https://img.shields.io/badge/Framework-FastAPI-red" alt="Framework: FastAPI">
  <img src="https://img.shields.io/badge/Database-PostgreSQL-blue" alt="Database: PostgreSQL">
  <img src="https://img.shields.io/badge/API-OpenAI-black" alt="API: OpenAI">
</div>
<div class="badges" align="center">
  <img src="https://img.shields.io/github/last-commit/coslynx/OpenAI-Request-Wrapper-MVP?style=flat-square&color=5D6D7E" alt="git-last-commit" />
  <img src="https://img.shields.io/github/commit-activity/m/coslynx/OpenAI-Request-Wrapper-MVP?style=flat-square&color=5D6D7E" alt="GitHub commit activity" />
  <img src="https://img.shields.io/github/languages/top/coslynx/OpenAI-Request-Wrapper-MVP?style=flat-square&color=5D6D7E" alt="GitHub top language" />
</div>

## 📑 Table of Contents
- 📍 Overview
- 📦 Features
- 📂 Structure
- 💻 Installation
- 🏗️ Usage
- 🌐 Hosting
- 📄 License
- 👏 Authors

## 📍 Overview

This repository hosts the backend for the AI Powered OpenAI Request Wrapper MVP. It's a Python application designed to simplify interactions with OpenAI's powerful language models.  The MVP functions as a bridge between users and the OpenAI API, making it easier to leverage AI for diverse tasks. 

## 📦 Features

| Feature           | Description                                                                                                        |
|--------------------|--------------------------------------------------------------------------------------------------------------------|
| Request Handling   | Accepts user requests for OpenAI API interactions, including model selection, prompt, and parameters.              |
| API Call Generation | Translates user requests into properly formatted OpenAI API calls, ensuring accurate encoding of model selection, prompt, parameters, and authentication details. |
| Response Processing | Parses and formats responses from the OpenAI API for easy understanding by the user, handling various response formats and extracting relevant information. |
| Database Integration |  Stores API keys and user preferences in a PostgreSQL database for efficient and personalized interactions.    |
| Authentication     | Uses JWTs for secure user authentication and authorization, ensuring safe access to the application and its resources. |

## 📂 Structure

```text
├── commands.json        # Defines available commands for the application
├── .env                # Stores environment variables securely
├── README.md            # This file
├── requirements.txt    # Lists all Python dependencies
├── startup.sh         # Script for setting up the application environment
├── main.py             # Main application entry point
└── src
    └── __init__.py       # Application initialization
    └── routers
        └── request_router.py  # Handles requests to the /request endpoint
    └── services
        └── openai_service.py  # Manages interactions with the OpenAI API
    └── models
        └── request.py      # Database model for storing requests and responses
    └── schemas
        └── request_schema.py # Pydantic schemas for validating API requests and responses
    └── database
        └── database.py     # Manages the database connection
        └── models.py      # Defines the database models for the application
    └── utils
        └── logger.py       # Provides a centralized logging system
    └── tests
        └── test_openai_service.py  # Unit tests for the openai_service
        └── test_request_router.py  # Unit tests for the request_router

```

## 💻 Installation

### 🔧 Prerequisites

- Python 3.9+
- PostgreSQL 14+
- Docker

### 🚀 Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/coslynx/OpenAI-Request-Wrapper-MVP.git
   cd OpenAI-Request-Wrapper-MVP
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Create the database:**
   ```bash
   createdb openai_request_wrapper
   ```
4. **Create the `pgcrypto` extension in the database:**
   ```bash
   psql -U postgres -d openai_request_wrapper -c "CREATE EXTENSION IF NOT EXISTS pgcrypto"
   ```
5. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   Replace placeholders in `.env` with your own values:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `DATABASE_URL`: Your PostgreSQL database connection string
   - `JWT_SECRET`: Your secret key for JWT token generation

## 🏗️ Usage

### 🏃‍♂️ Running the Application

1. **Start the application:**
   ```bash
   python main.py
   ```

## 🌐 Hosting

### 🚀 Deployment Instructions

For deployment, consider using a platform like Heroku or AWS.

**Heroku Deployment:**

1. **Install Heroku CLI:**
   ```bash
   npm install -g heroku
   ```
2. **Login to Heroku:**
   ```bash
   heroku login
   ```
3. **Create a new Heroku app:**
   ```bash
   heroku create openai-request-wrapper-production
   ```
4. **Set up environment variables:**
   ```bash
   heroku config:set OPENAI_API_KEY=YOUR_OPENAI_API_KEY
   heroku config:set DATABASE_URL=your_database_url_here
   heroku config:set JWT_SECRET=your_secret_key
   ```
5. **Deploy the code:**
   ```bash
   git push heroku main
   ```

## 📄 License

This Minimum Viable Product (MVP) is licensed under the [GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0/) license.

## 👏 Authors

- Drix10 
- Kais Radwan 

<p align="center">
  <h1 align="center">🌐 CosLynx.com</h1>
</p>
<p align="center">
  <em>Create Your Custom MVP in Minutes With CosLynxAI!</em>
</p>
<div class="badges" align="center">
  <img src="https://img.shields.io/badge/Developers-Drix10,_Kais_Radwan-red" alt="">
  <img src="https://img.shields.io/badge/Website-CosLynx.com-blue" alt="">
  <img src="https://img.shields.io/badge/Backed_by-Google,_Microsoft_&_Amazon_for_Startups-red" alt="">
  <img src="https://img.shields.io/badge/Finalist-Backdrop_Build_v4,_v6-black" alt="">
</div>