# Pulse and Pen

Pulse and Pen is a dynamic blogging website that allows users to create, edit, and share their blog posts. It provides an engaging platform for writers and readers to interact through comments and likes, fostering a community for creative expression.

## Features

- **User Authentication**: Secure login and registration system.
- **Create and Manage Blogs**: Users can write, edit, and delete their blog posts.
- **Interactive Engagement**: Readers can comment on and like blog posts.
- **Responsive Design**: Optimized for mobile, tablet, and desktop devices.
- **Admin Panel**: Administrative access for managing user posts and activities.

## Technologies Used

- **Framework**: Django
- **API**: Django REST Framework (DRF)
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Django's built-in authentication system
- **Version Control**: Git, GitHub

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Bilal-khan-1604/Pulse-and-Pen.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Pulse-and-Pen
   ```

3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up the database:
   - Update the database settings in `settings.py` to configure PostgreSQL.
   - Apply the migrations:
     ```bash
     python manage.py migrate
     ```

6. Create a superuser for admin access:
   ```bash
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

8. Open your browser and go to `http://127.0.0.1:8000` to access the application.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add your message here"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Create a pull request.

## Contact

If you have any questions or feedback, feel free to reach out:

- **GitHub**: [Bilal-khan-1604](https://github.com/Bilal-khan-1604)
- **Email**: mbk.muhammadbilalk@gmail.com
