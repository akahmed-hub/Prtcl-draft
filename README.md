# Bio Research Cursor (PrtclTech)

A comprehensive web application for biological research protocol building, data analysis, and visualization.

## Features

### V1 Core Features
- **Plan (Protocol Builder)**: AI-powered protocol generation with cross-referencing capabilities
- **Analyze**: Data analysis for qPCR and Western Blot data
- **Visualize**: Interactive data visualization with extensive customization options

## Tech Stack

- **Frontend**: React.js with Material-UI
- **Backend**: Django with Django REST Framework
- **Database**: PostgreSQL
- **Task Queue**: Celery with Redis
- **LLM Integration**: Anthropic Claude API
- **Containerization**: Docker

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.9+
- Node.js 16+

### Development Setup

1. **Clone and navigate to the project**
   ```bash
   cd prtcltech
   ```

2. **Start the development environment**
   ```bash
   docker-compose up -d
   ```

3. **Run database migrations**
   ```bash
   docker-compose exec backend python manage.py migrate
   ```

4. **Create superuser**
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin

## Project Structure

```
prtcltech/
├── frontend/          # React.js application
├── backend/           # Django application
├── docker-compose.yml # Development environment
└── README.md
```

## Environment Variables

Create a `.env` file in the root directory:

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/prtcltech

# Redis
REDIS_URL=redis://localhost:6379

# Anthropic API
ANTHROPIC_API_KEY=your-anthropic-api-key

# AWS S3 (for file storage)
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_STORAGE_BUCKET_NAME=your-bucket-name
```

## Development

### Frontend Development
```bash
cd frontend
npm install
npm start
```

### Backend Development
```bash
cd backend
pip install -r requirements.txt
python manage.py runserver
```

## API Documentation

The API documentation is available at `/api/docs/` when running the development server.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License
