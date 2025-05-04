#  Simple GUI Voting System

This repository contains the simple voting system built on Python. This project has Graphical User Interface(GUI) and implementation of databases.

## 👥 Our Team
- [Nursezim](https://github.com/argenkuz) (argenkuz): 🎨 Design and GUI.
- [Kirill Donetskov](https://github.com/kd0nwww) (kd0nwww): 🧠 Code and logic.

## 📂 Structure

- [user.py](/project/classes/user.py) : Contains the class that creates `User` instances.
- [votes.py](/project/classes/votes.py) : Contains the class that creates `Votes` instances.
- [candidate.py](/project/classes/candidate.py) : Class that creates `Candidate` instances.
- [election.py](/project/classes/election.py) : Class that creates `Election` instances.

- [base_dao.py](/project/dao/base_dao.py) : Contains the base DAO class (`Dao`) that is responsible to make CRUD operations with the database.
- [user_dao.py](/project/dao/user_dao.py) : Contains DAO class that inherits from `Dao` that is in base_dao.py.
- [votes_dao.py](/project/dao/votes_dao.py) : Contains DAO class that inherits from `Dao` that is in base_dao.py.
- [candidate_dao.py](/project/dao/candiadte_dao.py) : Contains DAO class that inherits from `Dao` that is in base_dao.py.
- [election_dao.py](/project/dao/election_dao.py) : Contains DAO class that inherits from `Dao` that is in base_dao.py.
- [controller.py](/project/controller.py) : This file makes the connection between logic and design.
- [login.py](/project/pyqt/login.py) : File with the design of login page.
- [main.py](/project/main.py) : File that launches the whole program.
- [model.py](/project/model.py) : File that contains the logic of program.
- [voting.py](/project/pyqt/voting.py) : File that contains the design of starting page.
- [vote.py](/project/pyqt/vote.py) : File that contains the design of vote page.


# 📂 Classes Directory

The `classes` directory contains the core classes used in the project. These classes define the main entities and their attributes, along with methods to interact with them.

## 🧑‍💻 User Class
The `User` class represents a user in the system. It includes attributes for user details and provides getter and setter methods for each attribute.

### Attributes
- `username`: The username of the user.
- `password`: The password of the user.
- `email`: The email address of the user.
- `phone_number`: The phone number of the user.

### Methods
- `get_username()`: Returns the username.
- `set_username(username: str)`: Sets the username.
- `get_password()`: Returns the password.
- `set_password(password: str)`: Sets the password.
- `get_email()`: Returns the email address.
- `set_email(email: str)`: Sets the email address.
- `get_phone_number()`: Returns the phone number.
- `set_phone_number(phone_number: str)`: Sets the phone number.
- `__str__()`: Returns a formatted string representation of the user.

---

## 🗳️ Votes Class
The `Votes` class represents a vote in the system. It includes attributes for the user, election, and candidate involved in the vote.

### Attributes
- `user_id`: The ID of the user who cast the vote.
- `election_name`: The name of the election.
- `candidate_id`: The ID of the candidate who received the vote.

### Methods
- `get_user_id()`: Returns the user ID.
- `set_user_id(user_id: int)`: Sets the user ID.
- `get_election_name()`: Returns the election name.
- `set_election_name(election_name: str)`: Sets the election name.
- `get_candidate_id()`: Returns the candidate ID.
- `set_candidate_id(candidate_id: int)`: Sets the candidate ID.

---

## 🗳️ Candidate Class
The `Candidate` class represents a candidate in an election. It includes attributes for the candidate's details.

### Attributes
- `candidate_id`: The unique ID of the candidate.
- `name`: The name of the candidate.
- `party`: The political party of the candidate.
- `election_name`: The election in which the candidate is participating.

### Methods
- `get_candidate_id()`: Returns the candidate ID.
- `set_candidate_id(candidate_id: int)`: Sets the candidate ID.
- `get_name()`: Returns the candidate's name.
- `set_name(name: str)`: Sets the candidate's name.
- `get_party()`: Returns the candidate's party.
- `set_party(party: str)`: Sets the candidate's party.
- `get_election_name()`: Returns the election name.
- `set_election_name(election_name: str)`: Sets the election name.

---

## 🗳️ Election Class
The `Election` class represents an election in the system. It includes attributes for the election's details.

### Attributes
- `election_name`: The name of the election.
- `start_date`: The start date of the election.
- `end_date`: The end date of the election.

### Methods
- `get_election_name()`: Returns the election name.
- `set_election_name(election_name: str)`: Sets the election name.
- `get_start_date()`: Returns the start date.
- `set_start_date(start_date: str)`: Sets the start date.
- `get_end_date()`: Returns the end date.
- `set_end_date(end_date: str)`: Sets the end date.
- `__str__()`: Returns a formatted string representation of the election.

## 🗄️ DAO Classes

The DAO (Data Access Object) classes are responsible for interacting with the database. They provide methods for CRUD (Create, Read, Update, Delete) operations and abstract the database logic from the rest of the application.

---

### 🛠️ BaseDao Class
The `BaseDao` class serves as the foundation for all DAO classes. It provides common methods for executing queries and managing database connections.

#### Attributes
- `db_path`: Path to the SQLite database file.

#### Methods
- `execute_query(query: str, params=None)`: Executes a query (e.g., `INSERT`, `UPDATE`, `DELETE`) with optional parameters and commits the transaction.
- `fetch_all(query: str, params=None)`: Executes a `SELECT` query and returns all results.
- `fetch_one(query: str, params=None)`: Executes a `SELECT` query and returns a single result.
- `close()`: Closes the database connection.

---

### 👤 UserDao Class
The `UserDao` class handles operations related to the `Users` table in the database. It inherits from `BaseDao`.

#### Methods
- `insert(user: User)`: Inserts a new user into the database.
- `find_by_username(username: str)`: Retrieves a user by their username.
- `find_by_email(email: str)`: Retrieves a user by their email.
- `get_all_users()`: Returns all users from the database.
- `update_password(email: str, new_password: str)`: Updates the password of a user identified by their email.

---

### 🗳️ VotesDao Class
The `VotesDao` class manages operations related to the `Votes` table. It inherits from `BaseDao`.

#### Methods
- `save_vote(username: str, election_name: str, candidate_id: int)`: Saves a vote to the database.
- `get_votes_by_election(election_name: str)`: Retrieves all votes for a specific election.
- `get_votes_by_user(username: str)`: Retrieves all votes cast by a specific user.

---

### 🗳️ CandidateDao Class
The `CandidateDao` class handles operations related to the `Candidates` table. It inherits from `BaseDao`.

#### Methods
- `insert(candidate: Candidate)`: Inserts a new candidate into the database.
- `find_by_id(candidate_id: int)`: Retrieves a candidate by their ID.
- `get_all_candidates()`: Returns all candidates from the database.
- `get_candidates_by_election(election_name: str)`: Retrieves all candidates participating in a specific election.

---

### 🗳️ ElectionDao Class
The `ElectionDao` class manages operations related to the `Elections` table. It inherits from `BaseDao`.

#### Methods
- `insert(election: Election)`: Inserts a new election into the database.
- `find_by_name(election_name: str)`: Retrieves an election by its name.
- `get_all_elections()`: Returns all elections from the database.
- `update_election_dates(election_name: str, start_date: str, end_date: str)`: Updates the start and end dates of an election.
- `delete_election(election_name: str)`: Deletes an election by its name.

## 🧠 Model Class

The `Model` class contains the core logic of the application. It handles user account creation, password validation, email validation, and sending password reset codes.

### Methods
- **`create_account(username: str, email: str, password: str, phone_number: str)`**:  
  Creates a new user account. Validates the input fields and returns success or error messages.

- **`is_strong_password(password: str)`**:  
  Checks if the password meets the strength requirements (minimum length, uppercase, lowercase, digit, special character).

- **`validate_email(email: str)`**:  
  Validates the format of an email address using a regular expression.

- **`is_valid_phone_number(phone_number: str)`**:  
  Validates the phone number format (e.g., starts with `0` and contains 10 digits).

- **`len_of_username(username: str)`**:  
  Returns the first 7 characters of the username.

- **`send_reset_password(email: str)`**:  
  Sends a 4-digit password reset code to the user's email. Returns the code for validation.

- **`validate_date_format(date_str: str)`**:  
  Validates if a date string matches the format `YYYY-MM-DD, HH:MM:SS`.

---

## 🔗 Controller Class

The `Controller` class connects the GUI with the application logic. It manages user interactions, updates the UI, and communicates with the `Model` and DAO classes.

### Methods
- **`show_main_window()`**:  
  Displays the main application window and initializes its buttons.

- **`show_login_window()`**:  
  Displays the login window and initializes its buttons.

- **`init_login_window_buttons()`**:  
  Connects buttons in the login window to their respective actions.

- **`set_visible()`**:  
  Hides specific labels in the login window.

- **`switch_to_tab_login()`**:  
  Switches to the login tab in the login window.

- **`switch_to_tab_create_account()`**:  
  Switches to the create account tab in the login window.

- **`on_cancel_create_account_clicked()`**:  
  Cancels the account creation process and switches to the login tab.

- **`login_account()`**:  
  Authenticates the user and displays login success or error messages.

- **`on_forgot_password_clicked()`**:  
  Switches to the "Forgot Password" tab in the login window.

- **`on_cancel_clicked()`**:  
  Closes the login window.

- **`create_account()`**:  
  Creates a new user account by validating input fields and saving the user to the database.

- **`on_send_code_clicked()`**:  
  Sends a password reset code to the user's email and updates the UI.

- **`on_check_code_clicked()`**:  
  Verifies the password reset code and switches to the password reset tab.

- **`change_password()`**:  
  Changes the user's password after validation.

### Notes
- The `Controller` class integrates with PyQt6 for GUI management.
- It uses DAO classes for database operations and the `Model` class for business logic.

### 🖼️ UML Diagram
![uml.png](icons/uml.png)

## 📊 Database Reports


## ⚙️ Installation and Usage
1. Clone the repository:
    ```bash
    git clone https://github.com/argenkuz/Shopping-system.git
    ```
2. Navigate to the project directory:
    ```bash
    cd project
    ```
3. Download all dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the script:
    ```bash
    python main.py
    ```