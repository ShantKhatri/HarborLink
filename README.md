# HarborLink

---

## Overview

**HarborLink** is an AI-powered middleware generator that transforms banking APIs into ONDC (Open Network for Digital Commerce) or OCEN (Open Credit Enablement Network) compliant interfaces.

Harnessing the capabilities of Google's Generative AI, it automates the parsing, mapping, and transformation of OpenAPI specifications into production-ready middleware.

---

## Features

- **API Specification Analysis**: Upload OpenAPI 3.0 specs and analyze endpoints and schemas.
- **AI-Powered Transformation**: Auto-map APIs to ONDC/OCEN using LLMs.
- **Framework Flexibility**: Generate adapters in FastAPI (Python) or Express.js (Node.js).
- **Compliance Engine**: Ensures your APIs meet ONDC or OCEN standards.
- **Project Management**: Save, manage, and revisit generated middleware.
- **Code Export**: Download ready-to-deploy code packages.
- **Interactive UI**: Clean, responsive React + Tailwind CSS frontend.
- **Authentication Layer**: Role-based access and login system for enhanced security.

---

## Stack

### 🖙 Backend

- **FastAPI**: Python-based web framework
- **SQLite**: Lightweight database
- **Google Generative AI**: For API transformation
- **Jinja2**: Code template rendering
- **JWT & OAuth2**: Secure authentication

### 🖜 Frontend

- **React** (with TypeScript)
- **Tailwind CSS**: Styling
- **Vite**: Fast frontend tooling

### DevOps

- **Docker & Docker Compose**: Containerization

---

## Installation

### Prerequisites

- Python 3.9+
- Node.js 14+
- Google Generative AI API Key

### Setup via Docker (Recommended)

```bash
git clone https://github.com/yourusername/HarborLink.git
cd HarborLink

# Create .env file
echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env

# Run the app
docker-compose up --build
```

> Access at: [http://localhost:8000](http://localhost:8000)

---

### 🖐 Manual Installation

#### Backend

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Frontend

```bash
cd frontend
npm install
```

#### Run Development Servers

```bash
# Start backend
uvicorn app.main:app --reload

# Start frontend (in separate terminal)
cd frontend
npm run dev
```

> Access:
>
> - Backend: `http://localhost:8000`
> - Frontend: `http://localhost:5173`

---

## Usage

### Authentication & Access

1. Sign up and log in to access the platform.
2. Role-based access:
   - **Admin**: Full access to projects and configurations.
   - **User**: Restricted to personal project workspace.

### Generate Middleware

1. Go to the **Generate** page.
2. Upload a valid OpenAPI 3.0 spec (JSON or YAML).
3. Choose:
   - Framework: FastAPI or Express.js
   - Target: ONDC or OCEN
4. Click **Generate Middleware**
5. Download the code or view the project in your dashboard.

### Manage Projects

- Browse all generated projects (based on role)
- Download or view code for any project

---

## 🗂 Project Structure

```
HarborLink/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   └── routes.py
│   ├── core/
│   │   ├── api_parser/
│   │   ├── middleware/
│   │   ├── transformation/
│   │   ├── validator/
│   │   └── utils/
│   ├── auth/
│   │   ├── jwt.py
│   │   ├── oauth.py
│   │   └── dependencies.py
│   ├── db/
│   │   ├── crud.py
│   │   ├── database.py
│   │   └── models.py
│   └── main.py
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.tsx
│   ├── index.html
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.ts
├── samples/
│   └── sample_api.json
├── logs/
├── .env
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

## API Documentation

Available at:

- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Key Endpoints

| Method | Endpoint                                | Description             |
| ------ | --------------------------------------- | ----------------------- |
| GET    | `/api/health`                           | Health check            |
| POST   | `/api/parser/analyze`                   | Analyze OpenAPI spec    |
| POST   | `/api/middleware/generate`              | Generate middleware     |
| GET    | `/api/middleware/download/{project_id}` | Download generated code |
| GET    | `/api/projects`                         | List all projects       |
| GET    | `/api/projects/{project_id}`            | Project details         |
| POST   | `/api/auth/login`                       | User login              |
| POST   | `/api/auth/signup`                      | User signup             |

---

## Testing

```bash
# Backend tests
pytest

# Frontend tests
cd frontend
npm test
```

---

## Contributing

We welcome contributions!

1. Fork this repo
2. Create a new branch: `git checkout -b feature/amazing-feature`
3. Commit: `git commit -m 'Add amazing feature'`
4. Push: `git push origin feature/amazing-feature`
5. Submit a Pull Request 🚀

---

## 🌐 Links

- 🔗 [ONDC](https://ondc.org/)
- 🔗 [OCEN](https://iSpirit.in/ocen)
- 🔗 [OpenAPI Spec](https://swagger.io/specification/)

