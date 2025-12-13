FULL SETUP GUIDE (LINUX & WINDOWS)

1. Install System Dependencies (Linux Only)
------------------------------------------
sudo apt update
sudo apt install libpq-dev python3-dev build-essential
# Needed for packages like psycopg2 to compile from source

2. Create and Activate Virtual Environment
------------------------------------------
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux
source venv/bin/activate

# Windows (cmd)
venv\Scripts\activate

# Windows (PowerShell)
. venv/Scripts/activate

3. Install Python Dependencies
------------------------------
pip install -r requirements.txt
# If psycopg2 fails, use psycopg2-binary in requirements.txt

4. Run the Application
----------------------
uvicorn app.main:app --reload

5. Database Migrations (Alembic)
---------------------------------
# Generate migration files automatically
alembic revision --autogenerate -m "create tables"

# Apply migrations to the database
alembic upgrade head

6. Freeze Installed Dependencies
--------------------------------
pip freeze > requirements.txt
# Saves all current Python packages into requirements.txt
