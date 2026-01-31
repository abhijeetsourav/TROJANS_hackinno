# AI-Powered Natural Language MongoDB Query System

A full-stack application integrating Ollama LLM with FastAPI backend and React frontend, orchestrated using Docker Compose.

## Project Overview

This project provides a containerized chat application that leverages Ollama's local LLM capabilities with a FastAPI backend and React frontend. The application uses WebSocket connections for real-time streaming responses and includes MongoDB integration for data retrieval.

## Architecture

The application consists of three main services:

- **Backend**: FastAPI application with LangChain integration
- **Frontend**: React application with Framework7 UI components
- **Ollama**: Local LLM service running the Phi3 model

## Prerequisites

- Docker and Docker Compose installed
- At least 8GB of RAM (recommended for running Ollama models)
- Sufficient disk space for Ollama models

## Project Structure

```
.
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   └── app/
│       └── tools/
│           └── tool.py
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── package-lock.json
│   ├── src/
│   └── public/
├── ollama/
│   └── ollama/
└── start-ollama.sh
```

## Getting Started

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <project-directory>
```

### 2. Build and Start Services

```bash
docker-compose up --build
```

This will:
- Build the backend and frontend containers
- Pull the Ollama image
- Start all services with proper networking

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Ollama Service**: http://localhost:11434

## Service Details

### Backend Service

- **Framework**: FastAPI
- **Port**: 8000
- **Features**:
  - WebSocket support for streaming responses
  - LangChain integration with Ollama
  - MongoDB tool integration
  - CORS enabled for cross-origin requests

**Key Dependencies**:
- FastAPI 0.75.0
- Uvicorn 0.15.0
- LangChain Community
- Ollama
- WebSockets

### Frontend Service

- **Framework**: React 17
- **UI Library**: Framework7
- **Port**: 3000
- **Features**:
  - Real-time chat interface
  - WebSocket connection to backend
  - Responsive mobile-first design

### Ollama Service

- **Model**: Phi3
- **Port**: 11434
- **Features**:
  - Local LLM inference
  - Persistent model storage
  - Health check monitoring

## API Endpoints

### REST Endpoints

- `GET /messages` - Get initial message

### WebSocket Endpoints

- `WS /ws` - WebSocket connection for real-time chat
  - Send text messages
  - Receive streaming responses
  - Ends with `**|||END|||**` marker

## Development

### Hot Reloading

Both frontend and backend support hot reloading during development:

- **Backend**: Volume mounted at `./backend/app:/code/app`
- **Frontend**: Volumes mounted for `src` and `public` directories

### Running Individual Services

```bash
# Backend only
docker-compose up backend

# Frontend only
docker-compose up frontend

# Ollama only
docker-compose up ollama
```

## Environment Variables

The application uses the following configuration:

- **OLLAMA_HOST**: localhost
- **OLLAMA_PORT**: 11434
- **Backend Port**: 8000
- **Frontend Port**: 3000

## Troubleshooting

### Ollama Service Not Starting

Check the health check status:
```bash
docker-compose ps
```

The Ollama service has a 120-second start period to allow for model loading.

### Connection Issues

Ensure all services are on the same Docker network (`ollama-docker`):
```bash
docker network inspect ollama-docker
```

### Port Conflicts

If ports 3000, 8000, or 11434 are already in use, modify the port mappings in `docker-compose.yml`.

## Stopping the Application

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Notes

- The Ollama service uses persistent volumes for model storage
- First run may take longer as models are downloaded
- WebSocket connections are maintained for continuous streaming
- The application uses the Phi3 model by default

## Future Enhancements

- Add authentication and authorization
- Implement conversation history
- Add support for multiple LLM models
- Enhance error handling and logging
- Add rate limiting
