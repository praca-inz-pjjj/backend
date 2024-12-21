# SafeKid API
## Description
This is a Django project that provides a REST API for a simple inżynierka project - SafeKid. It uses Django Rest Framework to provide the API endpoints.

## Deployments
TODO

## How to run the project (Devcontainer)
1. Clone the repository
2. Open project in Visual Studio Code
3. Install Docker Devcontainer extension
4. Reopen project in Devcontainer
5. Copy [.env.example](./.env-example) to [.env](./.env) in the root directory and fill it with required data:

    ```sh
    cp .env.example .env
    ```

6. Apply the migrations:

    ```sh
    python manage.py migrate
    ```

7. Run the server:

    ```sh
    python manage.py runserver
    ```
    
8. Navigate to [http://localhost:8000/](http://localhost:8000/) in your favorite web browser.

## How to run the project (Raw python)
1. Clone repository

2. Create and activate a virtual environment:

    ```sh
    $ python3 -m venv venv && source venv/bin/activate
    ```

3. Install the requirements:

    ```sh
    (venv)$ pip install -r requirements.txt
    ```

4. Copy [.env.example](./.env-example) to [.env](./.env) in the root directory and fill it with required data:

    ```sh
    (venv)$ cp .env.example .env
    ```

5. Apply the migrations:

    ```sh
    (venv)$ python manage.py migrate
    ```

6. Run the server:

    ```sh
    (venv)$ python manage.py runserver
    ```
    
7. Navigate to [http://localhost:8000/](http://localhost:8000/) in your favorite web browser.
