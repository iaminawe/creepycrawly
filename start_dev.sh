#!/bin/bash

# Start the backend server
cd backend/src && uvicorn main:app --reload --port 8000 &

# Start the frontend server
cd ../../frontend && npm run dev
