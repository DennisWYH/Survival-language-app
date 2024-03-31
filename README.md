# Project Name

Add a brief description of your project here.

## Installation

1. Clone the repository locally:

    ```bash
    git@github.com:DennisWYH/survival-language-app.git
    ```

2. Navigate to the project directory:

    ```bash
    cd <project-directory>
    ```
3. Make sure that python3 is installed
4. Create a vevn virtual environment for this project
    ```
    python -m venv ~./.venvs/languageApp
    ```

6. Install all project dependencies then using pip (ideally in a python virtual env):

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. Start the local development server:

    ```bash
    python manage.py runserver
    ```

2. If prompted to perform database migrations, run:

    ```bash
    python manage.py migrate
    ```

3. Create an admin user for testing:

    ```bash
    python manage.py createsuperuser
    ```

4. Visit `localhost:8000/admin` in your web browser to check out the admin url endpoints.

5. Visit `localhost:8000/card` in your web browser to test out the customer url endpoints.
