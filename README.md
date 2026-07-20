> [!Note]
> This is the backend of [Instrumate-Africa](https://github.com/FRANCISMUNGANGU/Instrumate)

## Build Instructions

To set up and build the project locally, follow these steps:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/bitflaw/instrumate-backend.git
    cd instrumate-backend
    ```

2. **Setup:**
   - Create and activate a virtual environment:
      ```bash
      python3 -m venv .venv
      source .venv/bin/activate
      cd instrumate
      pip install -r requirements.txt
      ```

3. **Run the backend server:**
   - **Locally**
    ```bash
    python manage.py runserver
    ```

> [!Warning]
> This project is not publicly accessible.

The [KSL Feedback Pipeline](https://github.com/bitflaw/KSL-Feedback-Pipeline).

## DATABASE SETUP

This project uses PostgreSQL as its primary database engine.

1. **To setup using docker**:
    ```bash
    $ docker compose up -d pgdb
    ```

    By default, the database is exposed on port `5432` on your machine.
    > [!Note]
    > This might collide with your host's instance of postgres server if it is running on the same port.
    > A solution would be to setup a .env file at the root of the project(instrumate) specifying the port you want the database
    > to run on.

    A seed file has been provided in the dropbox folder shared, and to setup the seed data, run the following command using the dump file:
    ```bash
    $ pg_restore -h localhost -p <PORT-SPECIFIED> -U {postgres/your user} -d <DATABASE> seed.dump
    ```

2. **To stop the database container**:
    ```bash
    $ docker compose down pgdb
    ```

3. **If you have made any changes to your local database**, and you wish for the data to be used by other members of the team:
    ```bash
    $ pg_dump -Fc <DATABASE_NAME> -U <USER> -h localhost -p <PORT> > seed.dump
    ```
    Then upload that dump file to the dropbox.
