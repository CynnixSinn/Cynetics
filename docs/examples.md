# Cynetics Examples

Real-world examples of projects built with Cynetics.

## Example 1: Task Management API

### Description

```bash
python cynetics.py --description "
Build a REST API for task management with:
- User authentication (JWT)
- CRUD operations for tasks
- Task assignment to users
- Priority levels (low, medium, high)
- Due dates and reminders
- Search and filtering
- Comprehensive test coverage
" --stack '{
  "language": "python",
  "framework": "fastapi",
  "database": "postgresql",
  "orm": "sqlalchemy"
}'
```

### Generated Files

```
workspace/
├── main.py                      # FastAPI application
├── models/
│   ├── user.py                  # User model
│   └── task.py                  # Task model
├── routes/
│   ├── auth.py                  # Authentication endpoints
│   ├── tasks.py                 # Task CRUD endpoints
│   └── users.py                 # User endpoints
├── services/
│   ├── auth_service.py          # Auth business logic
│   └── task_service.py          # Task business logic
├── database.py                  # Database connection
├── config.py                    # Configuration
├── requirements.txt
├── tests/
│   ├── test_auth.py
│   ├── test_tasks.py
│   └── conftest.py
└── README.md
```

### Key Features Generated

- JWT authentication with refresh tokens
- Password hashing with bcrypt
- Input validation with Pydantic
- Database migrations with Alembic
- Comprehensive API documentation
- Unit and integration tests

## Example 2: CLI Tool

### Description

```bash
python cynetics.py --description "
Create a CLI tool for managing development environments:
- List all environments
- Create new environment with template
- Delete environment
- Export/import environment configuration
- Colorful terminal output
- Progress indicators
" --stack '{
  "language": "python",
  "cli_framework": "click"
}'
```

### Generated Files

```
workspace/
├── devenv.py                    # Main CLI
├── commands/
│   ├── list.py
│   ├── create.py
│   ├── delete.py
│   └── export.py
├── utils/
│   ├── config.py
│   └── output.py
├── tests/
├── setup.py
└── README.md
```

## Example 3: Web Dashboard

### Description

```bash
python cynetics.py --description "
Build a web dashboard for monitoring server metrics:
- Real-time CPU, memory, disk usage
- Historical data with charts
- Alert configuration
- Multi-server support
- Responsive design
" --stack '{
  "frontend": "react",
  "backend": "node",
  "database": "mongodb",
  "realtime": "websocket"
}'
```

### Generated Structure

```
workspace/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── MetricsChart.jsx
│   │   │   └── ServerList.jsx
│   │   ├── App.jsx
│   │   └── index.js
│   ├── package.json
│   └── README.md
├── backend/
│   ├── src/
│   │   ├── routes/
│   │   ├── models/
│   │   ├── websocket.js
│   │   └── server.js
│   ├── package.json
│   └── README.md
└── docker-compose.yml
```

## Example 4: Data Pipeline

### Description

```bash
python cynetics.py --description "
Create an ETL pipeline that:
- Extracts data from CSV and JSON files
- Transforms data with validation
- Loads to PostgreSQL database
- Runs on schedule
- Sends email alerts on failure
- Provides progress tracking
" --stack '{
  "language": "python",
  "framework": "airflow"
}'
```

### Generated DAG

```python
# Automatically generated Airflow DAG
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'cynetics',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'data_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
) as dag:
    extract = PythonOperator(...)
    transform = PythonOperator(...)
    load = PythonOperator(...)
    
    extract >> transform >> load
```

## Example 5: Microservice

### Description

```bash
python cynetics.py --description "
Build a user authentication microservice:
- Register/login endpoints
- Email verification
- Password reset
- Rate limiting
- API key management
- Docker deployment
" --stack '{
  "language": "go",
  "framework": "gin",
  "database": "postgres",
  "cache": "redis"
}'
```

### Generated Structure

```
workspace/
├── main.go
├── handlers/
│   ├── auth.go
│   └── users.go
├── models/
│   └── user.go
├── middleware/
│   ├── auth.go
│   └── ratelimit.go
├── config/
│   └── config.go
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Example 6: Chrome Extension

### Description

```bash
python cynetics.py --description "
Create a Chrome extension for productivity:
- Block distracting websites
- Set time limits for sites
- Track time spent per site
- Weekly reports
- Customizable block lists
" --stack '{
  "language": "javascript",
  "framework": "chrome-extension-api"
}'
```

### Generated Files

```
workspace/
├── manifest.json
├── popup/
│   ├── popup.html
│   ├── popup.js
│   └── popup.css
├── background.js
├── content.js
├── options/
│   ├── options.html
│   └── options.js
└── icons/
```

## Tips for Best Results

### 1. Be Specific

**Bad:**
```
"Make a web app"
```

**Good:**
```
"Build a recipe sharing web application where users can:
- Upload recipes with photos and ingredients
- Rate and comment on recipes
- Search by ingredients or cuisine type
- Create meal plans for the week
- Generate shopping lists from meal plans"
```

### 2. Specify Constraints

```bash
--stack '{
  "constraints": [
    "Must work offline",
    "Bundle size < 500KB",
    "Support mobile browsers",
    "WCAG 2.1 AA compliant"
  ]
}'
```

### 3. Include User Stories

```
"As a teacher, I want to create quizzes online so that I can assess students remotely.
As a student, I want to take quizzes on any device so that I can learn anywhere.
As an admin, I want to view analytics so that I can track student progress."
```

### 4. Mention Integrations

```bash
--stack '{
  "integrations": [
    "Stripe for payments",
    "SendGrid for emails",
    "AWS S3 for file storage"
  ]
}'
```

## Running Examples

All examples are in the `examples/` directory:

```bash
# Run an example
cd examples/01-task-api
cat description.txt | python ../../cynetics.py --description "$(cat -)"

# View output
ls output/
```

## Contributing Examples

Have a great Cynetics project? Share it!

1. Create example in `examples/XX-your-example/`
2. Include `description.txt` with the prompt
3. Include `expected-output.md` with what it generates
4. Submit a pull request
