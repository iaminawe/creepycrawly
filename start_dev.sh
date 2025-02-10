#!/bin/bash

# Navigate to the project root directory
cd "$(dirname "$0")"

# Debug: Print current directory
echo "Current directory: $(pwd)"

# Ensure Python is installed
if ! command -v python &> /dev/null
then
    echo "Python could not be found. Please install Python and ensure it is added to the system PATH."
    exit 1
fi

# Navigate to the backend directory and start the backend server
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/main.py &

# Debug: Print current directory
echo "Current directory: $(pwd)"

# Navigate to the scripts directory and start the scripts server
cd ../scripts
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Navigate back to the project root directory
cd ..

# Debug: Print current directory
echo "Current directory: $(pwd)"

# Navigate to the frontend directory and start the frontend development server
cd frontend && npm run dev

# Debug: Print current directory
echo "Current directory: $(pwd)"

# Wait for any process to exit
wait

# Exit the script when any of the processes exit
exit $?
