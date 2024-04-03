# Project Name

Add a brief description of your project here.

## Installation

### 👉 Clone the repository locally:
```bash
$ git@github.com:DennisWYH/languageApp.git
$ cd languageApp
```
### 👉 Make sure `python3` is installed
### 👉 Create a vevn virtual environment and start it 
```bash
$ python -m venv ~./.venvs/languageApp
$ source ~./.venvs/languageApp/bin/activate
```
### 👉 Install all project dependencies using `pip` (ideally in a `python` virtual env):
```bash
$ pip install -r requirements.txt
```
## Running the Application
1. Export DEBUG = True
2. Export DEVELOPMENT_MODE = True

3. Start the local development server:

    ```bash
    python manage.py runserver
    ```

4. If prompted to perform database migrations, run:

    ```bash
    python manage.py migrate
    ```

5. Create an admin user for testing:

    ```bash
    python manage.py createsuperuser
    ```

6. Visit `localhost:8000/admin` in your web browser to check out the admin url endpoints.

7. Visit `localhost:8000/card` in your web browser to test out the customer url endpoints.
