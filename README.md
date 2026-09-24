# Gamer Matchmaking API

A RESTful backend API built with FastAPI designed to connect gamers. This platform allows users to create profiles, link their favorite games, swipe on other players, and automatically form matches when two users like each other.

## 🚀 Tech Stack

*   **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
*   **Database:** SQL Database (via [SQLAlchemy](https://www.sqlalchemy.org/) ORM)
*   **Data Validation:** Pydantic
*   **Authentication:** OAuth2 with JWT (JSON Web Tokens) & Argon2 password hashing
*   **Server:** Uvicorn

## 🛠️ Features

*   **Secure Authentication:** User registration and login flow using securely hashed passwords and JWT access tokens.
*   **Profile Management:** Update bios and upload profile pictures securely to the local file system.
*   **Game Associations:** Link users to specific games via a many-to-many database relationship.
*   **Swiping & Discovery:** Fetch a list of potential matches (excluding already swiped profiles).
*   **Matchmaking Logic:** Automatically detects reciprocal "likes" and generates a Match record.

## 💻 Local Setup & Installation

Follow these steps to run the API locally on your machine.

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/GamerTinder.git
cd GamerTinder/backend
```

**2. Create and activate a virtual environment**
```bash
# Create the environment
python -m venv env

# Activate (Windows)
.\env\Scripts\activate
# Activate (Mac/Linux)
source env/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Environment Variables**
Create a `.env` file in the root directory and add the following variables:
```ini
DATABASE_URL=sqlite:///./test.db  # Or your PostgreSQL/MySQL connection string
SECRET_KEY=your_super_secret_key_here
```

**5. Run the Application**
```bash
uvicorn app:app --port 8080 --reload  (use port 8080 for Frontend integration)
```
The server will start on `http://127.0.0.1:8080`. You can access the interactive Swagger API documentation by navigating to `http://127.0.0.1:8080/docs`.

## 📍 Key API Endpoints

*   **`POST /register/`**: Create a new user account and receive an access token.
*   **`POST /login/`**: Authenticate and receive a JWT access token.
*   **`PATCH /update_profile/`**: Update user bio and profile image (requires auth).
*   **`GET /profiles`**: Fetch a list of discoverable users (requires auth).
*   **`POST /swipe/`**: Like or pass on another user. Triggers match creation if mutual (requires auth).
*   **`GET /matches/`**: Retrieve a list of successful matches (requires auth).
*   **`POST /games/`**: Update the list of games associated with the user (requires auth).