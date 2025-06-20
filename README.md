# Vulnerability Management System

![Lint with pylint](https://github.com/aman18sharma/SecureSphere/actions/workflows/pylint.yml/badge.svg) ![Tech Stack](https://img.shields.io/badge/Tech%20Stack-Python%20%7C%20JavaScript%20%7C%20CSS%20%7C%20HTML-blue)
 <!-- Optional: Add a diagram if available -->
# SecureSphere Architecture

```mermaid
graph TD
    A[Frontend] -->|API Calls| B[Backend]
    B -->|HTTP| C[OLLAMA AI]
    B -->|CRUD| D[(SQLite Database)]
    A -->|Static Assets| E[CDN]

    subgraph Frontend
        A --> F[React]
        A --> G[Vite]
        A --> H[Chart.js]
    end

    subgraph Backend
        B --> I[FastAPI]
        B --> J[SQLAlchemy]
        B --> K[Pydantic]
    end

    subgraph AI Layer
        C --> L[LLAMA3]
        C --> M[Mistral]
    end
```
A full-stack application for tracking, analyzing, and assessing software vulnerabilities with AI-powered analysis.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Deployment](#deployment)
- [License](#license)

## Features

### Frontend
- 📊 Interactive vulnerability dashboard
- 🔍 Detailed vulnerability view with AI assessment
- 📁 JSON file upload functionality
- 📱 Responsive design with modern UI
- 📈 Real-time data visualization

### Backend
- 🚀 RESTful API with FastAPI
- 💾 SQLite database integration
- 🤖 OLLAMA AI integration for vulnerability analysis
- ⬆️ File upload handling
- 🔄 CORS support

## Tech Stack

### Frontend
| Technology | Purpose |
|------------|---------|
| ![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react) | Frontend framework |
| ![Vite](https://img.shields.io/badge/Vite-B73BFE?style=flat&logo=vite) | Build tool |
| ![React Router](https://img.shields.io/badge/React_Router-CA4245?style=flat&logo=react-router) | Navigation |
| ![Axios](https://img.shields.io/badge/Axios-5A29E4?style=flat&logo=axios) | HTTP client |
| ![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=flat&logo=chart.js) | Data visualization |

### Backend
| Technology | Purpose |
|------------|---------|
| ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi) | API framework |
| ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite) | Database |
| ![OLLAMA](https://img.shields.io/badge/OLLAMA-FF6600?style=flat) | AI processing |
| ![Pydantic](https://img.shields.io/badge/Pydantic-920000?style=flat) | Data validation |

## Installation

### Prerequisites
- Node.js 18+
- Python 3.10+
- OLLAMA (for local AI)
- Docker (optional)

```bash
# Clone repository
git clone [https://github.com/aman18sharma/SecureSphere](https://github.com/aman18sharma/SecureSphere)
cd SecureSphere
```
## Backend Setup
```bash
cd backend
python -m venv venv

# Linux/MacOS
source venv/bin/activate

# Windows
.\venv\Scripts\activate

pip install -r requirements.txt

uvicorn main:fast_app

```
## Frontend Setup
```
```bash
cd frontend
npm install

```
