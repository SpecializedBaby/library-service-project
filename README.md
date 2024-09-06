# Library Service

There is a library in my city, where you can borrow books and pay for your borrowings using cash, depending on the days you read the book. The online management system for book borrowings. The system optimize the work of library administrators and make the service much more user-friendly.

## Overview
Library Service is a Django-based application designed to manage a library system. It allows users to borrow and return books, tracks borrowings, and sends notifications on key events. The system includes features such as JWT authentication, admin and user roles, and Telegram bot integration for notifications.

## Features
- **User Authentication**: Custom user model using email and password for authentication.
- **Book Management**: Admins can add, update, or delete books. All users can view the list of available books.
- **Borrowing System**: Users can borrow books, with inventory management and borrowing tracking.
- **Permissions**: 
  - Only admins can create/update/delete books.
  - All users can list books.
  - Only authenticated users can borrow books.
- **Filtering**: Allows filtering borrowings by active status, user ID, and more.
- **Notification System**: Integration with Telegram bot to send notifications on borrowing events.
- **Admin Dashboard**: Django Admin integration for managing books, users, and borrowings.

## Installation

### Prerequisites
- Python 3.8+
- Django 3.2+
- PostgreSQL (or another supported database)
- `pip` for package management

### Setup Instructions

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/library_service.git
    cd library_service
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the environment variables:**
    - Create a `.env` file in the root directory of the project.
    - Add the following variables (modify with your actual settings):
      ```plaintext
      SECRET_KEY=your_secret_key
      DEBUG=True
      ALLOWED_HOSTS=localhost, 127.0.0.1
      DATABASE_URL=postgres://user:password@localhost:5432/dbname
      TELEGRAM_BOT_TOKEN=your_telegram_bot_token
      TELEGRAM_CHAT_ID=your_telegram_chat_id
      ```

5. **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

6. **Create a superuser for accessing the admin panel:**
    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

8. **Access the application:**
    - API: `http://localhost:8000/api/`
    - Admin panel: `http://localhost:8000/admin/`

## Usage

### Book Management
- **Admins** can manage books through the Django Admin panel or via the API.
- **Users** can view available books and borrow them via the API.

### Borrowing Books
- Users can borrow books as long as there is available inventory.
- Borrowings are tracked, and inventory is updated automatically.

### Returning Books
- Users can return books via the API, which will update the inventory and borrowing records.

### Filtering Borrowings
- Use query parameters like `is_active=true` or `user_id=1` to filter borrowing records in the API.

### Notifications
- The system sends Telegram notifications on borrowing events. Ensure your bot is set up correctly to receive these notifications.

## Testing

### Running Tests
To run the test suite, use the following command:
```bash
python manage.py test
