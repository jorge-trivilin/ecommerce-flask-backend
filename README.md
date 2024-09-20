# E-commerce Flask Backend

## Project Description

This project is a backend system for a simple e-commerce platform built with Flask. It provides RESTful API endpoints for user management, product management, shopping cart functionality, and order processing. The system includes user authentication, role-based access control, and data persistence using SQLite.

![Version](https://img.shields.io/badge/version-1.0.0-blue)

*Jorge Trivilin.* 

## Video

[![Thumbnail do Vídeo](https://img.youtube.com/vi/UPkdGN9MUZg/0.jpg)](https://www.youtube.com/watch?v=UPkdGN9MUZg)

## Features

- User Management:
  - User registration and login
  - Secure password hashing
  - JWT-based authentication
- Product Management:
  - CRUD operations for products (Admin only)
  - Product listing and details viewing (All users)
- Shopping Cart:
  - Add products to cart
  - View cart contents
  - Remove items from cart
- Order Processing:
  - Place orders
  - View order history
  - Retrieve order details
- Admin Functionality:
  - Manage products (Add, Edit, Delete)
- Data Persistence:
  - SQLite database for storing users, products, carts, and orders
- Error Handling:
  - Comprehensive error handling for invalid inputs, unauthorized access, etc.
- Testing:
  - Unit tests for critical functions

## Technology Stack

- Python 3.12
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- SQLite
- pytest (for testing)

## Project Structure

```
ecommerce-flask-backend/
│
├── .github/
│   └── workflows/
│       ├── Build, Test, Lint & Format.yml
│       └── Lint.yml
│
├── app/
│   ├── routes/
│   ├── __init__.py
│   ├── error_handlers.py
│   ├── extensions.py
│   └── models.py
│
├── migrations/
│   ├── versions/
│   ├── README
│   ├── alembic.ini
│   ├── env.py
│   └── script.py.mako
│
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_carts.py
│   ├── test_orders.py
│   └── test_products.py
│
├── .gitignore
├── .pylintrc
├── README.md
├── app.db
├── buildspec.yml
├── config.py
├── dev-requirements.txt
├── Dockerfile
├── Makefile
├── pyproject.toml
├── requirements.txt
├── run_build.sh
├── run.py
└── seed_data.py
```
## Key Files and Directories

- `.github/workflows/`: Contains CI/CD configuration for GitHub Actions.
- `app/`: Main application package.
  - `routes/`: Contains route definitions for different parts of the application.
  - `error_handlers.py`: Defines error handling mechanisms.
  - `extensions.py`: Initializes Flask extensions.
  - `models.py`: Defines database models.
- `migrations/`: Contains database migration files managed by Alembic.
- `tests/`: Contains all unit tests for the application.
- `.env`: Environment variables file (not tracked by git).
- `.gitignore`: Specifies intentionally untracked files to ignore.
- `.pylintrc`: Configuration file for Pylint.
- `README.md`: Project documentation and overview.
- `app.db`: SQLite database file.
- `buildspec.yml`: Build specification for CI/CD in AWS CodeBuild 
- `config.py`: Configuration settings for the application.
- `dev-requirements.txt`: Development dependencies.
- `Dockerfile`: Instructions for building a Docker image of the application.
- `Makefile`: Contains commands for common operations.
- `pyproject.toml`: Configuration file for Python tools like Black and Ruff.
- `requirements.txt`: Production dependencies.
- `run_build.sh`: Script to run the build process.
- `run.py`: Script to run the application.
- `seed_data.py`: Script to populate the database with initial data.

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/e-commerce-backend.git
   cd e-commerce-backend
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory and add the following:
   ```
   FLASK_APP=app
   FLASK_ENV=development
   SECRET_KEY=your_secret_key_here
   JWT_SECRET_KEY=your_jwt_secret_key_here
   ```

5. Initialize the database:
   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```

## Running the Application

To run the application in development mode:

```
flask run
```

The API will be available at `http://localhost:5000`.

## API Endpoints

### Authentication
- `POST /api/auth/register`: Register a new user
- `POST /api/auth/login`: Login and receive access token

### Products
- `GET /api/products`: List all products
- `GET /api/products/<id>`: Get product details
- `POST /api/products`: Add a new product (Admin only)
- `PUT /api/products/<id>`: Update a product (Admin only)
- `DELETE /api/products/<id>`: Delete a product (Admin only)

### Cart
- `GET /api/cart`: View cart contents
- `POST /api/cart`: Add item to cart
- `DELETE /api/cart/<product_id>`: Remove item from cart

### Orders
- `POST /api/orders`: Place an order
- `GET /api/orders/history`: View order history
- `GET /api/orders/<order_id>`: Get order details

## Using the Makefile

The project includes a Makefile to simplify common development tasks. Here are some useful commands:

- `make install`: Install all dependencies (both production and development)
- `make lint`: Run linting checks on the code
- `make test`: Run the test suite
- `make format`: Format the code using autopep8
- `make clean`: Clean up generated files and caches

To use these commands, simply run `make <command>` in the project root directory.

## Explanation of the Makefile

The Makefile defines several tasks:

- `install`: Installs both production and development dependencies
- `install-prod`: Installs only production dependencies
- `install-dev`: Installs development dependencies
- `lint`: Runs Pylint on the `app` and `tests` directories
- `test`: Runs pytest with specific flags for efficient testing
- `format`: Uses autopep8 to format Python files and commits changes if any
- `clean`: Removes Python cache files and directories

These tasks help standardize development processes and make it easier to perform common actions.

## GitHub Actions Workflow

The project uses GitHub Actions for continuous integration. The workflow is triggered on push events and performs the following steps:

1. Sets up the Python environment
2. Caches pip packages for faster subsequent runs
3. Installs dependencies
4. Runs linting checks
5. Executes the test suite
6. Formats the code and pushes any changes

This workflow ensures that code quality is maintained and tests pass with every push to the repository.

## AWS CodeBuild Buildspec

The `buildspec.yml` file defines the build process for AWS CodeBuild. It consists of three phases:

1. **Pre-build**: Sets up the environment, logs into Amazon ECR, and installs dependencies.
2. **Build**: Runs linting and tests, then builds and tags a Docker image.
3. **Post-build**: Pushes the Docker image to Amazon ECR and generates an artifact.

This process automates the build and deployment of the application in an AWS environment, ensuring consistency and reliability in the deployment process.

## Possible Improvements

- Implement user roles and permissions for finer-grained access control
- Add product categories and search functionality
- Implement inventory management
- Add payment integration
- Enhance test coverage with integration and end-to-end tests

## License

This project is licensed under the MIT License.
