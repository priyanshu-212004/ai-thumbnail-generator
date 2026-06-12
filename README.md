# AI Thumbnail Generator

An AI-powered YouTube Thumbnail Generator built using FastAPI, SQLModel, SQLite, AsyncIO, and ImageKit. The application allows users to generate multiple thumbnail variations from a text prompt and manage them through a modern web interface.

---

## Features

* Generate AI-powered YouTube thumbnails from text prompts
* Multiple thumbnail styles

  * Bold Dramatic
  * Clean Minimal
  * Vibrant Energetic
* Asynchronous thumbnail generation
* REST API architecture
* SQLite database for job and thumbnail tracking
* Image hosting and CDN delivery via ImageKit
* Real-time job status updates
* Frontend interface built with HTML, CSS, and JavaScript

---

## Tech Stack

### Backend

* Python
* FastAPI
* SQLModel
* SQLite
* AsyncIO
* Uvicorn

### Frontend

* HTML
* CSS
* JavaScript

### Third-Party Services

* Hugging Face Inference API
* ImageKit CDN

---

## Project Structure

```text
THUMBNAIL/
│
├── backend/
│   ├── services/
│   │   ├── generator.py
│   │   ├── huggingface_service.py
│   │   └── imagekit_service.py
│   │
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── routes.py
│   └── main.py
│
├── frontend/
│   └── index.html
│
└── README.md
```

---

## System Architecture

1. User enters a thumbnail prompt through the frontend.
2. Frontend sends a request to FastAPI backend.
3. Backend creates a job and stores it in SQLite.
4. Async workers process thumbnail generation.
5. AI service generates thumbnail images.
6. Images are uploaded to ImageKit.
7. Image URLs are saved in the database.
8. Frontend displays generated thumbnails and job status.

---

## Installation

### Clone Repository

```bash
git clone https://github.com/priyanshu-212004/ai-thumbnail-generator.git
cd ai-thumbnail-generator
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux / Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file inside the backend directory.

```env
HUGGINGFACE_API_KEY=your_api_key

IMAGEKIT_PRIVATE_KEY=your_private_key
IMAGEKIT_PUBLIC_KEY=your_public_key
IMAGEKIT_URL_ENDPOINT=your_url_endpoint

DATABASE_URL=sqlite:///thumbnail.db
```

---

## Run Backend

Navigate to backend folder:

```bash
cd backend
```

Start FastAPI server:

```bash
python -m uvicorn main:app --reload
```

Backend will run at:

```text
http://127.0.0.1:8000
```

---

## Run Frontend

Navigate to frontend folder:

```bash
cd frontend
```

Open:

```text
index.html
```

using a browser or Live Server extension.

---

## API Workflow

### Create Job

```http
POST /jobs
```

Creates a thumbnail generation job.

### Get Job Status

```http
GET /jobs/{job_id}
```

Returns job progress and generated thumbnails.

---

## Key Concepts Implemented

* REST API Development
* Async Programming with AsyncIO
* Database Design using SQLModel
* Environment Variable Management
* Cloud Image Storage
* Background Task Processing
* Error Handling and Logging
* Full-Stack Integration

---

## Future Improvements

* User Authentication
* Custom Thumbnail Templates
* Drag-and-Drop Image Upload
* AI Face Replacement
* Multiple AI Model Support
* Cloud Database Integration
* Docker Deployment

---

## Author

Priyanshu

B.Tech Computer Science Engineering

GitHub: https://github.com/priyanshu-212004
