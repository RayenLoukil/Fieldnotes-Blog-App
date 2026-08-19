# 📝 Fieldnotes

[![Python](https://img.shields.io/badge/Python-3.13%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.3.1-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9.3-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18.6-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **A modern full-stack technical blogging platform where authenticated users can publish technical notes, browse other authors' work, and manage their profiles.**

Built as a hands-on full-stack engineering project with **FastAPI + React + TypeScript**, focusing on clean architecture, authentication, API design, database management, and a polished frontend experience.

---

## ✨ Features

- 🔐 **Authentication**
  - User registration & login
  - JWT-based authentication
  - Secure password hashing
  - Protected API routes

- 📝 **Technical Posts**
  - Create, read, update & delete posts
  - Post ownership & authorization
  - Paginated feeds
  - Individual post pages

- 👤 **User Profiles**
  - Browse users and profiles
  - View a user's posts
  - Update account information
  - Upload profile pictures

- 🎨 **Modern UI**
  - Responsive React interface
  - Reusable UI components
  - Light / dark mode
  - Client-side routing
  - Form validation

- 🗄️ **Database & Migrations**
  - SQLAlchemy ORM
  - PostgreSQL support
  - Async database operations
  - Alembic migrations

- ⚡ **API**
  - RESTful JSON API
  - Automatic JWT handling
  - Validation & error handling
  - Health-check endpoint

---

## 🛠️ Tech Stack

### Backend

| Technology | Purpose |
|---|---|
| 🐍 **Python** | Backend language |
| ⚡ **FastAPI** | REST API framework |
| 🗃️ **SQLAlchemy** | ORM & database access |
| 🐘 **PostgreSQL** | Relational database |
| 🔄 **Alembic** | Database migrations |
| 🔑 **JWT / OAuth2** | Authentication |
| 🔒 **pwdlib** | Password hashing |
| ✅ **Pydantic** | Data validation |

### Frontend

| Technology | Purpose |
|---|---|
| ⚛️ **React** | UI framework |
| 📘 **TypeScript** | Type-safe development |
| ⚡ **Vite** | Frontend tooling |
| 🎯 **TanStack Query** | Server-state management |
| 🐻 **Zustand** | Client-state management |
| 📡 **Axios** | HTTP client |
| 📝 **React Hook Form** | Form management |
| ✅ **Zod** | Schema validation |
| 🎨 **Tailwind CSS** | Styling |

---

## 🏗️ Architecture

```text
Fieldnotes
│
├── 🐍 Backend
│   ├── main.py
│   ├── auth.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── image_utils.py
│   │
│   ├── router/
│   │   ├── posts.py
│   │   └── users.py
│   │
│   └── alembic/
│       └── versions/
│
└── ⚛️ Frontend
    └── src/
        ├── components/
        ├── hooks/
        ├── pages/
        ├── store/
        ├── lib/
        └── types/
```

---

## 🚀 Getting Started

### 1️⃣ Clone the repository

```bash
git clone <repository-url>
cd fieldnotes
```

### 2️⃣ Set up the backend

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

```bash
# Windows
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure environment variables

Create a `.env` file:

```env
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> ⚠️ Never commit real secrets or credentials to Git.

### 4️⃣ Run database migrations

```bash
alembic upgrade head
```

### 5️⃣ Start the API

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

### 6️⃣ Start the frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at:

```text
http://localhost:5173
```

---

## 🔌 API

The backend exposes a REST API under:

```text
/api
```

Main resources:

```text
/api/users
/api/posts
/api/health
```

Authentication uses **Bearer JWT tokens**, automatically attached to authenticated frontend requests.

---

## 🗄️ Database

Database schema changes are managed with **Alembic**.

```bash
# Apply migrations
alembic upgrade head
```

The current schema includes:

```text
Users
├── id
├── username
├── email
├── password_hash
└── image_file

Posts
├── id
├── title
├── content
├── id_user
└── created_at
```

Posts are linked to their authors through a foreign-key relationship.

---


## Working on : (roadmap)

### Authentication

- [ ] Complete password reset flow
- [ ] Email-based password reset
- [ ] Background email tasks

### Storage

- [ ] Migrate profile image storage to AWS S3

### Testing

- [ ] Add Pytest test suite
- [ ] Add API endpoint tests
- [ ] Add authentication/authorization tests
- [ ] Add image-processing tests

### Deployment

- [ ] Deploy to VPS
- [ ] Configure Nginx
- [ ] Configure SSL/TLS
- [ ] Production environment configuration

### Infrastructure

- [ ] Dockerize backend
- [ ] Dockerize frontend
- [ ] Define production container workflow

---

## Security Notes

- Never commit `.env`.
- Never commit real database credentials.
- Never commit production `SECRET_KEY` values.
- Use a cryptographically secure secret key in production.
- Backend authorization must always be enforced independently of frontend restrictions.
- Review Alembic migrations before applying them to production databases.

---

## License

This project is licensed under the **MIT License**.

See [`LICENSE`](LICENSE) for the complete license text.

---

### 👨‍💻 Built with Python & React

**Fieldnotes — Write. Learn. Share.**
