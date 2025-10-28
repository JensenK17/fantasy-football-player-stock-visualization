# Quick Start Guide

## Prerequisites

✅ **Dependencies Installed**
- Python 3.9+ installed
- All Python packages installed globally

## Run the Application

### Backend (Flask API)

Open a terminal in the project root and run:

```bash
# Option 1: Run directly
cd backend
python app.py

# Option 2: Run with custom script
python backend/run.py
```

The backend will start on `http://localhost:5000`

### Frontend (React App)

Open a NEW terminal in the project root and run:

```bash
cd frontend
npm install
npm start
```

The frontend will start on `http://localhost:3000`

## Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## Troubleshooting

If you get import errors:
```bash
# Make sure you're in the backend directory
cd backend

# Python should find the modules in current directory
python app.py
```

If npm install fails:
```bash
cd frontend
rm -rf node_modules  # Windows: Remove-Item node_modules -Recurse
npm install
```

## Testing

Test the PPR Calculator:
```bash
python -c "from backend.data.ppr_calculator import calculate_ppr_points; print('Working!')"
```

Test backend is working:
```bash
curl http://localhost:5000/
```

