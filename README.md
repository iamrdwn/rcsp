# CHINAR Kashmir RCSP Management Web App

This is a web application to help CHINAR Kashmir manage their Remote Child Sponsorship Program (RCSP). The app will help the NGO track the children being sponsored, their donors, and manage donations.

Read more about CHINAR Kashmir's Remote Child Sponsorship Program [here](https://chinarkashmir.org/remote-child-sponsorship-program-rcsp/)

## Features

- Manage children data
- Manage donor data
- Map donations from an individual donor to children
- User authentication and authorization
- Visualisations to show statistics about the program performance
- Report generation and Export as Excel

## Tech Stack

- FastAPI
- SQLAlchemy
- Alembic
- Jinja
- HTML/CSS
- SQLite


## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/iamrdwn/rcsp.git
    cd rcsp
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    Create a `.env` file and add your configuration. Example:
    ```
    DATABASE_URL=sqlite:///./test.db
    SECRET_KEY=your_secret_key
    GOOGLE_CLIENT_ID=<gcp_auth_client>
    GOOGLE_CLIENT_SECRET=<gcp_auth_secret>
    ```
5. Run database migrations:
    ```bash
    alembic upgrade head
    ```

6. Start the development server:
    ```bash
    uvicorn app.main:app --reload
    ```

7. Open your browser and go to `http://127.0.0.1:8000`

## Running Tests

```bash
pytest
```


## Contributing

Contributions are welcome. We have started this project as part of the [Kashmir Remote Collective](https://www.remotecollective.one), if you would like to contribute, please open an issue or submit a pull request.

## License
MIT
