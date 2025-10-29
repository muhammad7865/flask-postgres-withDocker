# 1. Use an official Python runtime as a parent image
FROM python:3.10-slim-bullseye

# 2. Set the working directory in the container
WORKDIR /app

# 3. Install pipenv (we only need it for one command)
RUN pip install pipenv

# 4. Copy the Pipfile AND the lock file
COPY Pipfile Pipfile.lock ./

# 5. NEW APPROACH: Convert the Pipfile.lock to a requirements.txt
#    This bypasses all of pipenv's Python version checks
RUN pipenv requirements > requirements.txt

# 6. Install all dependencies using reliable, standard pip
#    This WILL put gunicorn in the system $PATH
RUN pip install -r requirements.txt

# --- NEW LINE ADDED ---
# 7. Install the PostgreSQL driver (missing from Pipfile)
RUN pip install psycopg2-binary
# --- END OF NEW LINE ---

# 8. Install gunicorn (missing from Pipfile)
RUN pip install gunicorn

# 9. Copy the rest of the application source code
COPY . .

# 10. Expose the port the app runs on (defined in .env or default)
EXPOSE 5000

# 11. Define the command to run the app using python -m
#     This is more robust than relying on $PATH
CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

