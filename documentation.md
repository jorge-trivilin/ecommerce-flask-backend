# Ecommerce-Flask-Backend
---

## Assignment
---

**Problem Statement:**  
Create a backend system for a simple e-commerce platform where users can register, view a list of products, add products to a cart, and place an order. You should also implement basic user authentication and ensure that users can only view and manipulate their own data.

**Requirements:**

- **User Management:**
  - The persona for Users should be able to register, log in, and manage their account.
  - Passwords should be securely stored (e.g., hashed).

- **Product Management:**
  - The persona for Admins should be able to add, edit, and remove products.
  - Regular users should be able to view a list of products and details of each product.

- **Cart and Order Management:**
  - Users should be able to add products to a cart.
  - Users should be able to view their cart and place an order.
  - Once an order is placed, the cart should be cleared, and the order details should be saved.

- **Data Persistence:**
  - Store user, product, cart, and order data in a file-based database (e.g., JSON, SQLite).

- **Testing:**
  - Write basic unit tests for persona critical functions like user registration, product addition, and order placement.

- **Error Handling:**
  - Handle common errors such as invalid inputs, unauthorized access, and unavailable products.

- **Version Control:**
  - Use Git to manage your project. Make regular commits and document your work in a README file.

**Tested Competencies:**

- **Problem-Solving Skills:**
  - The challenge requires designing and implementing a solution that involves multiple components (users, products, orders), testing the candidate’s ability to break down complex problems using Software Engineering best practices.

- **Programming Fundamentals:**
  - The candidate will need to use object-oriented design, design patterns, basic data structures (e.g., lists, dictionaries), control flow, and functions to manage the application’s logic.

- **Code Quality:**
  - The candidate’s ability to write clean, readable code is tested by the need to organize different components of the application, adhere to DRY (Don't Repeat Yourself) principles, and provide comments where necessary indicating input parameters, return, and ensuring function signatures contain variable annotations.

- **Testing and Debugging:**
  - Writing unit tests for key functions assesses testing skills, while debugging the implementation is necessary to ensure the application works as expected. TDD is validated and preferred by reviewing the commit history.

- **Language Proficiency:**
  - Demonstration of Python proficiency by implementing the application with correct syntax, using appropriate libraries, and following best practices (e.g., comments, variable annotations, list comprehensions, etc.).

- **Version Control:**
  - Use of Git can be assessed by reviewing the solution’s commit history indicating branch management and overall use of basic version control.

- **Communication Skills:**
  - Explaining the solution approach in the well-formatted README.md documents their implementation and should describe any assumptions made. (Often problems are not well-formed and require a bit of decision-making. Use this as an opportunity to show how well you identify missing or incomplete information and press forward with a solution that is under test.)

- **Adaptability and Learning:**
  - If unfamiliar with certain aspects (like user authentication or writing tests), use the README.md to identify areas you had to look up to learn on the fly as a demonstration of the ability to adapt.

**Challenge Instructions:**

- Anticipated Time Required: Less than 4 hours
- Tools Required: Python, the IDE of your choosing, internet access, and git.

**Deliverables:**

1. The codebase in a compressed file containing the entire git repository.  
   § NOTE: Be sure to include the .git file for inspection of commits.
   
2. A README.md file containing at a minimum a general project description, how to set up and run the application, how to test the application, any assumptions made, and any learnings you had to do to design and/or implement the solution.
   
3. A description of the approach taken and any trade-offs or decisions made during implementation.  
   § NOTE: Consider discussing the use of Object-Oriented design, leveraging Python Protocols over inheritance (recommended), Design Patterns (see here for an overview of design patterns), and anything you believe would be a good callout for this challenge illustrating your programming, systems thinking, and general expertise.

**Rubric:**  
Your code submission will be assessed based on the quality of the solution in addressing the 8 competencies identified above in the “Tested Competencies” section.

## Project Structure
---

```plaintext
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
├── .env
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
## Stack
---

- Language: Python
- Web Framework: Flask
- Database: SQLite
- Auth:
- ORM: SQLAlchemy
- Testing: pytest
- Version control: Github

## Files / Modules
---

### `app/models.py`

**associated requirements:**
- User Management
- Product Model
- (Cart, CartItem, Order, OrderItem models)

**docs:**
- https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/
- https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage.html
- https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html


This file defines the database schema for a simple e-commerce backend using SQLAlchemy, an Object-Relational Mapping (ORM) library for Python.

This file encapsulates six main models: User, Product, Cart, CartItem, Order, and OrderItem.

User Model:
This class represents our application users. It includes fields for id, username, email, and password_hash. The is_admin boolean flag distinguishes between regular users and administrators. We implemented set_password and check_password methods for secure password handling using Werkzeug's security functions. The User model has relationships with Cart and Order models.

Product Model:
Represents items available for purchase. It contains fields for id, name, description, price, and stock. This model is central to our e-commerce functionality, storing all necessary product information.

Cart Model:
Represents a user's shopping cart. It has a one-to-one relationship with the User model and a one-to-many relationship with CartItem. This structure allows each user to have a single cart containing multiple items.

CartItem Model:
Acts as a junction between Cart and Product models. It includes quantity field to track how many of a particular product are in a cart. This model enables us to handle the many-to-many relationship between carts and products efficiently.

Order Model:
Captures completed orders. It includes fields for total price and order date, with a relationship to the User who placed the order. The one-to-many relationship with OrderItem allows an order to contain multiple products.

OrderItem Model:
Similar to CartItem, but for completed orders. It stores the quantity and price of each product in an order, allowing us to maintain historical pricing information even if product prices change later.

#### Mapped column

During development, Pylance was reporting the following error:

```python
"mapped_column" is unknown import symbolPylancereportAttributeAccessIssue
(import) mapped_column: Unknown
```
Pylance did not recognize the mapped_column symbol as a valid import.

Mapped_column was introduced in SQLAlchemy 2.0 as an alternative to traditional Column for declarative mappings in ORM. This new type is designed to improve integration with typing tools such as MyPy and Pylance by providing a more accurate representation of how attributes behave at runtime. The lack of recognition by Pylance suggests that the project may be using an earlier version of SQLAlchemy, or that Pylance is still configured to only recognize the traditional Column format rather than the new mapped_column.

After switching to `mapped_column`, I encountered the following error:

```
Type "Column" is not assignable to declared type "Mapped[int]"
  "Column" is not assignable to "Mapped[int]"PylancereportAssignmentType
Incompatible types in assignment (expression has type "Column", variable has type "Mapped[int]")mypyassignment
(class) Integer
A type for int integers.
```
The error occurs because the Column type is not assignable to the declared type Mapped[int].

The Mapped type was introduced in SQLAlchemy 2.x to improve the typing of mapped columns. This type provides a more accurate representation of the type of columns, but requires the use `mapped_column` instead of Column. The error indicates that there is a mismatch between the expected data type (Mapped[int]) and the provided data type (Column).

`mapped_column` was introduced in SQLAlchemy 2.0 as a replacement for Column in the context of declarative mappings in the ORM. It is designed to improve integration with typing tools like MyPy and Pylance, providing a more accurate representation of how attributes behave at runtime.

https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html

####  Password Hash Validation Issue

During development, the following error was encountered:

```python
Argument 1 to "check_password_hash" has incompatible type "None"; expected "str"mypyarg-type
Argument of type "None" cannot be assigned to parameter "pwhash" of type "str" in function "check_password_hash"
  "None" is not assignable to "str"PylancereportArgumentType
```
The check_password_hash function is designed to validate a provided password against a stored hashed password. However, if self.password_hash is None, it cannot be passed as a valid argument to the function, which results in a type mismatch error. This situation might arise if the password hash is not defined for a user or in cases where object initialization is incorrect.

To address this issue, a preliminary check should be added to verify if self.password_hash is None before attempting to use it in the check_password_hash function. If self.password_hash is None, the function should return False to indicate that password validation cannot be performed due to the absence of a valid hash.

#### Handling Deprecated utcnow Method

The following deprecation warning was encountered:

```python
The method "utcnow" in class "datetime" is deprecated
  Use timezone-aware objects to represent datetimes in UTC; e.g. by calling .now(datetime.timezone.utc)Pylance
(method) def utcnow() -> datetime
Construct a UTC datetime from time.time().

```
The `datetime.utcnow()` method is deprecated. It’s recommended to use timezone-aware datetime objects to represent dates and times in UTC. The `utcnow()` method does not include timezone information, which is less precise and may lead to issues in applications where timezone-aware datetimes are critical.

The solution was to replace the usage of `datetime.utcnow()` with `datetime.now(datetime.timezone.utc)` to create a timezone-aware datetime object representing the current time in UTC.

### `app/extensions.py`

**This module initializes and configures extensions for the Flask application.** It creates instances of commonly used extensions, which can be imported and used throughout the application.

- db: An instance of SQLAlchemy used for database interactions and Object-Relational Mapping (ORM). SQLAlchemy simplifies database operations by providing a high-level interface to work with databases in a Pythonic way.

- jwt: An instance of JWTManager used for managing JSON Web Tokens (JWT) for authentication and authorization. JWTManager facilitates secure handling of authentication tokens, enabling secure user sessions and API access control.

This file was created because of a `sqlite3.OperationalError: no such table: user`when trying to run make test. 

There were two instances of SQLAlchemy being created: 

- One in `app/__init__.py` with `db = SQLAlchemy()`
- Another in `app/models.py` with `db: SQLAlchemy = SQLAlchemy()`.

As result, the models were beign registered with a different db instance. When i called `db.create_all()` in the test, it didn't create the tables for the models, because they were associated with a different db instance.

The solution was to create  a single db instance to be used across all aplication. 

To fix this, i needed to ensure only one instance of SQLAlchemy were used throughout the application and that both `app/__init__.py` and `app/models.py` were refering to the same db object.

The first learning here is that project structure is fundamental in larger Flask applications. Separating extension initialization into its own file helps avoid circular imports and keeps code organized.

#### Insights regarding the creation of `extensions.py`

- By creating a single instance of SQLAlchemy in `extensions.py`, the **Singleton pattern** was implemented for Flask extensions. This ensures that the entire application uses the same database connection.

  In Object-oriented programming, the singleton pattern is a software design pattern that restricts the instantiation of a class to a singular instance. One of the well-known "Gang of Four" design patterns, which describes how to solve recurring problems in object-oriented software.[1] The pattern is useful when exactly one object is needed to coordinate actions across a system.

  https://en.wikipedia.org/wiki/Singleton_pattern

- Moving extension initialization to a separate file is an effective technique for resolving circular import issues, which are common in larger Flask applications.

- It has become clear the importance to maintain consistency in how extensions are imported and used throughout the project. Using from `app.extensions import db` instead of creating new instances ensures that all application components are working with the same objects. 

- I have learned how to interpret SQLAlchemy errors, specifically recognizing that a "no such table" error generally indicates a problem in database configuration or initialization, not necessarily in the model code.

My `app/__init__.py` looked like this: 

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.routes import routes_bp
from config import Config, TestConfig
from app.error_handlers import register_error_handlers

db = SQLAlchemy()
jwt = JWTManager()


def create_app(config_class=Config):
```
After creating the `extensions.py` file, the initialization file was changed to use the extensions:

```python
from flask import Flask
from flask_migrate import Migrate  # type: ignore
from config import Config
from app.extensions import db, jwt
from app.routes import routes_bp
from app.routes.orders import orders_bp
from app.routes.cart import cart_bp
from app.error_handlers import register_error_handlers

# from app.models import User, Product, Cart, CartItem, Order, OrderItem


def create_app(config_class=Config) -> Flask:
```
#### JWTManager

- By including the JWTManager in `extensions.py`, we are preparing the application to use **JWT-based authentication** consistently across the project. This is particularly useful in an e-commerce application, where we need to manage user sessions, secure administration routes, and possibly integrate with front-end clients or external services securely.

- JSON Web Tokens, or JWTs, are an authentication mechanism used to securely transmit information between a client and a server in JSON format.

- This information can be verified and trusted because it is digitally signed with the HMAC algorithm or a public/private key pair using RSA or ECDSA

- When a user successfully logs in, JWTManager can generate a JWT token that contains encoded information about the user (such as their ID or role).

- In p**rotected routes**, JWTManager checks the validity of tokens sent in requests, ensuring that only authenticated users can access certain resources.

- JWTManager handles token expiration, increasing security by limiting the lifetime of an authenticated session.

- Provides decorators like @jwt_required() that can be used to protect specific routes.

- Helps protect applications against common authentication-related attacks by securely managing token creation and verification.

https://www.freecodecamp.org/news/jwt-authentication-in-flask/

Summary: The inclusion of **JWTManager** in this extensions file centralizes authentication configuration, making it easier to maintain and update security settings in a single location.

### `app/error_handlers.py`

**associated requirements:**
- Error Handling

- I implemented the error_handlers.py as a global handler with a function called `register_error_handlers` who defines error handlers for different types of executions. 

- It specifically registers error handlers for common HTTP status codes:

  - 400 Bad Request
  - 404 Not Found
  - 405 Method Not Allowed
  - 500 Internal Server Error

- Handles generic exceptions to ensure that all errors are logged
  and returned in a standardized JSON format.

- For unhandled exceptions, logs the error to the server log and returns a generic 500 error response. 

> from flask documentation: When building a Flask application you will run into exceptions. If some part of your code breaks while handling a request (and you have no error handlers registered), a “500 Internal Server Error” (InternalServerError) will be returned by default.

After the creation, i registered the `register_error_handlers` inside `app/__init__`:

```python
def create_app(config_class=Config) -> Flask:
    """
    Creates and configures an instance of the Flask application.

    Args:
        config_class (Type[ConfigType]): The configuration class to use for the application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)
    Migrate(app, db)

    # Register blueprints
    app.register_blueprint(cart_bp)
    app.register_blueprint(routes_bp)
    app.register_blueprint(orders_bp)

    # Register global error handlers
    register_error_handlers(app)

    return app
```
#### Pylance

Pylance was saying that none of the functions were accessible, example;

```
"bad_request" is not accessed Pylance
(function) def bad_request(e: Unknown) -> tuple[Response, Literal[400]]
No quick fixes available
```
- This is expected because these functions are registered as error handlers using the Flask application's `errorhandler` method. These handlers `@app.errorhandler` is a Flask decorator that we use to register functions that handle specific or general errors.

- The decorator is applied directly to the Flask app instance, and does not need to be imported separately because it is a method of the Flask class.

https://flask.palletsprojects.com/en/2.3.x/errorhandling/

#### HTTPException

- `HTTPException`: A Werkzeug exception class that is the basis for HTTP exceptions in Flask. This allows to appropriately handle specific HTTP errors, such as 404 Not Found or 400 Bad Request.

When an error occurs in Flask, an appropriate HTTP status code will be returned. 400-499 indicate errors with the client’s request data, or about the data requested. 500-599 indicate errors with the server or application itself. 

https://werkzeug.palletsprojects.com/en/3.0.x/exceptions/

#### `jsonify()`

- The jsonify() function is useful in Flask apps because it automatically sets the correct response headers and content type for JSON responses, and allows you to easily return JSON-formatted data from your route handlers. This makes it easier and more convenient to create APIs that return JSON data.

https://www.geeksforgeeks.org/use-jsonify-instead-of-json-dumps-in-flask/

### `app/__init__.py`

- Flask: The main Flask class for creating an application.
- Migrate: Used to manage and apply migrations to the database, allowing to update the database schema as the model evolves.
- Config: A class that contains application configuration (e.g. secret keys, database details).
- db and jwt: Instances of SQLAlchemy and JWTManager, respectively, configured in app.extensions. They are used to manage the database and JWT authentication.
- routes_bp, orders_bp, cart_bp: Blueprints that define groups of routes and handlers for different parts of the application.
- register_error_handlers: Function to register custom error handlers in the application.

```python
def create_app(config_class=Config) -> Flask:
    """
    Creates and configures an instance of the Flask application.

    Args:
        config_class (Type[ConfigType]): The configuration class to use for the application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)
    Migrate(app, db)

    # Register blueprints
    app.register_blueprint(cart_bp)
    app.register_blueprint(routes_bp)
    app.register_blueprint(orders_bp)

    # Register global error handlers
    register_error_handlers(app)

    return app
```
### Routes

#### `app/routes/auth.py`

**associated requirements:**
- User Management

https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage.html

The `auth.py` module defines routes for authentication in the backend of an e-commerce using Flask and the Flask-JWT-Extended extension for token-based authentication.

- Blueprint: Used to create a modular set of routes.
- request: To access the HTTP request data.
- jsonify: To create JSON responses.
- create_access_token: Flask-JWT-Extended function to create JWT access tokens.
- db and User: Imported from the model to interact with the database and represent the user model.


- Created a blueprint called "auth": `auth_bp = Blueprint("auth", __name__)`

> doc: Flask uses a concept of blueprints for making application components and supporting common patterns within an application or across applications. Blueprints can greatly simplify how large applications work and provide a central means for Flask extensions to register operations on applications. A Blueprint object works similarly to a Flask application object, but it is not actually an application. Rather it is a blueprint of how to construct or extend an application.

https://flask.palletsprojects.com/en/3.0.x/blueprints/

Routes: 

- Registration: Allows new users to register, ensuring that the username and email are unique. `def register():`
- Login: Allows registered users to log in by providing a JWT token if the credentials are valid. `def login():`

#### `app/routes/cart.py`

**associated requirements:**
- Cart and Order Management (cart operations)

The module `cart.py` defines routes for shopping cart-related operations in an e-commerce using Flask and Flask-JWT-Extended for token-based authentication. 

- Blueprint: Used to create a modular route module.
- jsonify: Creates JSON responses.
- request: To access HTTP request data.
- jwt_required: Decorator that protects the route, requiring a valid JWT token.
- get_jwt_identity: Gets the user's identity from the JWT token.
- db, User, Product, Cart, and CartItem: Models and database instances.

- Created a blueprint called cart_bp: `cart_bp = Blueprint("cart_bp", __name__, url_prefix="/cart")`

- Created to organize routes related to the shopping cart. The /cart prefix is ​​added to all routes registered in this blueprint.

- Using `@jwt_required()` to protect all routes. A decorator to protect a Flask endpoint with JSON Web Tokens. Any route decorated with this will require a valid JWT to be present in the request (unless optional=True, in which case no JWT is also valid) before the endpoint can be called.

- `def view_cart():` Gets the current user's cart items and returns them in JSON format.

- `def add_to_cart():` Adds a product to the user's cart, creating a cart if necessary and updating the quantity if the product is already in the cart.

- `def remove_from_cart(product_id)`: Removes a specific product from the user's cart.

#### `app/routes/orders.py`

**associated requirements:**
- Cart and Order Management

The orders.py module defines routes for order-related operations in an e-commerce application. 

- Created a blueprint called orders_bp: `orders_bp = Blueprint("orders", __name__, url_prefix="/orders")`

- Used to organize and record routes related to orders.

- `def place_order():` Processes the order based on the items in the user's cart. Create a new order, associate the order items and clear the cart, Returns a success message with order ID or an error if the cart is empty.

- `def get_order_history():` Retrieves the list of all user orders, ordered from newest to oldest. Returns the list of user requests with summary information.

- `def get_order_details(order_id):` Retrieves details for a specific order, including all associated items. Returns detailed order information or an error if the order is not found.

#### `app/routes/products.py`

**associated requirements:**
- Product Management

This module manages product administration for the e-commerce platform using Flask. It offers endpoints to list, retrieve, add, edit, and delete products. The module includes operations restricted to administrators for product management.

- Uses Flask to create routes and handle HTTP requests/responses.
- Uses Flask-JWT-Extended for token-based authentication.
- Imports data models (Product, User) and the SQLAlchemy db object.

- Created a blueprint called products_bp: `products_bp = Blueprint("products", __name__)`

- Allows to organize routes related to products.

- `def admin_required(fn)`: This is a custom decorator that checks if the current user has administrator privileges. Uses JWT to identify the user and checks if they are an administrator. And if it is not admin, it returns a 403 (Forbidden) error.


##### Routes and functions:

- `def get_products():` Lists all products in the database and returns a JSON with details of all products.

- `def get_product(product_id):` Returns details for a specific product. If the product does not exist, it returns a 404 error.

- `def add_product():` Adds a new product to the database and requires administrator privileges using the decorator created. Verifies that name and price were provided.

- `def edit_product(product_id):` Updates an existing product and requires administrator privileges. Allows partial updating (only provided fields are updated).

- `def delete_product(product_id):` Removes a product from the database and requires administrator privileges. Handles product not found errors and database issues.

##### Error Handling

Each function includes specific error handling. Uses try/except to catch and handle database exceptions and returns appropriate HTTP status codes (200, 201, 400, 404, 500) depending on the result of the operation.

##### Security:

Add, edit, and delete operations are protected by the admin_required decorator and uses get_or_404 to search for products, automatically throwing a 404 error if not found.

#### `app/routes/__init__.py`

The __init__.py module has the function of initializing the Flask application routing and configuring the route structure of the e-commerce application. This file is essential for defining and organizing routes and for ensuring that the different functionalities of the application are well integrated.

- Created a blueprint called routes_bp: `routes_bp = Blueprint("routes", __name__)`

- This blueprint servers as the main blueprint creation for the routes and blueprints created before. 

The __init__.py module is the central point for configuring the application's routes. It creates a main blueprint, called routes_bp, which serves as a container for the other blueprints. Through this master blueprint, the other blueprints are registered and configured to be available at specific URLs.

- Authentication Routes are registered with the `/auth` prefix, which means that all authentication-related routes will be available under this path. For example, a login route, will be accessible at `/auth/login`.

- Product Routes do not have a specific prefix registered in the main blueprint, because these routes will be directly under the `/products `path. This facilitates direct access to product management operations, such as listing and editing, through URLs such as /products and `/products/<id>`.

Cart Routes, similarly, are the routes associated with the shopping cart and are registered under the `/cart` path, allowing managing of items in the cart through related URLs.

### Tests

**associated requirements:**
- Testing

#### `config.py`

The `config.py` file contains configuration classes for the Flask application. It defines settings for different environments, such as production and testing. These settings control various aspects of the Flask app's behavior, including database connections, secret keys, and testing options.

`class Config:`

```python
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "another-secret-key"

```

- `SECRET_KEY`: The key used by Flask to sign cookies and protect against tampering. It retrieves the key from environment variables or falls back to "you-will-never-guess" if not set.
- `SQLALCHEMY_DATABASE_URI`: The URI for the SQLAlchemy database connection. It creates a path to an SQLite database file named app.db located in the base directory.
- `SQLALCHEMY_TRACK_MODIFICATIONS`: Disables Flask-SQLAlchemy's modification tracking feature, which is not needed and can be inefficient.
- `JWT_SECRET_KEY`: The secret key used for encoding and decoding JSON Web Tokens (JWTs). It retrieves the key from environment variables or falls back to "another-secret-key" if not set.

`class TestConfig(Config):`

```python
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "test-secret-key"
    JWT_SECRET_KEY = "test-jwt-secret-key"

```
**Inherits from Config and overrides settings specifically for the testing environment.**

- `TESTING`: Enables the Flask testing mode, which provides better error handling and debugging features.
- `SQLALCHEMY_DATABASE_URI`: Uses an in-memory SQLite database (sqlite:///:memory:) for testing. This is temporary and does not persist between test runs.
- `SECRET_KEY`: Sets a different secret key for testing purposes.
- `JWT_SECRET_KEY`: Sets a different JWT secret key for testing purposes.

#### `tests/__init__.py`

The `__init__.py` of the tests/ module configures the environment necessary to run tests for the Flask application. It includes logging configuration, creating a test client, and managing the test database lifecycle.

1. Principal components:

```python
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
```
- Configures logging for debugging, which is useful for viewing detailed information while running tests.
- Defines the format of log messages.

```python
@pytest.fixture(scope="module")
def test_client():
    """
    Fixture for creating a test client for the application.

    Sets up the application and creates a test client for making requests.
    Also sets up and tears down the database schema for testing.

    Returns:
        FlaskClient: The test client instance.
    """
    app = create_app(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

```
- Sets up the application using `create_app(TestConfig)`.
- Creates a test client to make requests during tests.
- Initializes the database schema before running tests.
- Cleans up the database schema after tests complete.
- Automatically used by pytest for running tests.
- Provides a test client for interacting with the application in tests.

#### `tests/test_auth.py`

The test_auth.py module provides unit tests for authentication-related features in the Flask app, specifically focusing on user registration and login. It includes test cases to ensure that the authentication endpoints function correctly under various scenarios.

##### Fixtures
Fixtures are used to set up and provide resources needed for tests. They ensure a consistent and isolated test environment.

```python
@pytest.fixture
def app():
```

- Sets up the Flask application and initializes the database tables before yielding the app instance. After the tests, it removes the database session and drops all tables to clean up.

- Provides the Flask application instance for use in test functions.

```python
@pytest.fixture(scope="function")
def session(app):
```

- Creates a fresh `SQLAlchemy` database session for each test function, ensuring tests do not interfere with one another. It also sets up and tears down the database schema for each test.
- Provides a new SQLAlchemy session for individual tests, ensuring isolation.

```python
@pytest.fixture
def client(app):
```

- Provides a test client that simulates HTTP requests to the application.
- Allows making requests to the app and receiving responses during tests.

```python
@pytest.fixture
def new_user_data():
```
- Provides sample data for user registration.
- Supplies test data for creating a new user.

```python
@pytest.fixture
def sample_user(session):
```
- Creates a sample user in the database if it does not already exist.
- Provides a sample user for authentication tests.

##### Test Cases

```python
def test_register_user(client, new_user_data):
```
- Tests successful user registration and verifies that the user is correctly added to the database.

```python
def test_register_existing_username(client, sample_user):
```

- Tests the scenario where a registration attempt is made with an existing username.

```python
def test_register_existing_email(client, sample_user):
```
- Tests the scenario where a registration attempt is made with an existing email address.


```python
def test_login_success(client, sample_user):
```
- Tests successful login with valid credentials and checks for the presence of an access token in the response.

```python
def test_login_invalid_credentials(client):
```
- Tests login failure when invalid credentials are provided.

#### `tests/test_carts.py`

The `test_cart.py` module provides unit tests for cart-related functionality in the Flask application. It ensures that cart operations like adding, removing, and viewing products work correctly, and handles scenarios involving empty carts and non-existent items.

##### Fixtures
Fixtures set up and provide the necessary resources for the tests, ensuring a consistent and isolated testing environment.

```python
@pytest.fixture
def app():
```
- Sets up a Flask application instance with a test database. It creates the database tables, logs the registered routes, and cleans up by removing the database session and dropping all tables after tests are completed.
- Provides the Flask application instance for use in test functions.

```python
@pytest.fixture
def client(app):
```
- Provides a test client that simulates HTTP requests to the Flask application.
- Allows making requests and receiving responses during tests.

```python
@pytest.fixture
def auth_headers(app, client):
```
- Creates a test user, logs them in, and provides authorization headers for authenticated requests.
- Supplies authorization headers with a Bearer token for making authorized requests in the tests.

```python
@pytest.fixture
def sample_product(app):
```
- Adds a sample product to the database for testing cart operations.
- Returns the created product instance for use in the tests.

##### Test Cases

```python
def test_view_empty_cart(client, auth_headers):
```
- Tests the endpoint for viewing an empty cart. Verifies that the cart is empty by making a GET request and checking the response.
- Ensures that the response status code is 200 and the cart data is an empty list.

```python
def test_add_to_cart(client, auth_headers, sample_product):
```
- Tests adding a product to the cart. Verifies that the product is added with the correct quantity by making a POST request and checking the cart contents.
- Ensures the response status code is 200 and the cart contains the product with the expected quantity.

```python
def test_remove_from_cart(client, auth_headers, sample_product):
```
- Tests removing a product from the cart. Adds a product to the cart, removes it, and verifies that the cart is empty afterwards.
- Ensures the response status code is 200 and the cart is empty after removal.

```python
def test_remove_nonexistent_item(client, auth_headers):
```
- Tests the removal of a non-existent item from the cart. Ensures a 404 Not Found error is returned when attempting to remove an item that does not exist in the cart.
- Checks that the response status code is 404 and the error message is appropriate.

```python
def test_add_existing_product(client, auth_headers, sample_product):
```
- Tests adding an existing product to the cart and updating its quantity. Adds the product twice with different quantities and verifies that the quantity is updated correctly.
- Ensures the response status code is 200 and the cart reflects the updated quantity.

```python
def test_clear_cart(client, auth_headers, sample_product):
```
- Tests clearing the entire cart. Adds a product to the cart, clears it, and verifies that the cart is empty.
- Ensures the response status code is 200 and the cart is empty after clearing.


#### `tests/test_orders.py`

The `test_orders.py` module provides unit tests for order-related functionalities in the Flask application. It ensures that operations like placing orders, retrieving order history, and fetching specific order details work as expected under different scenarios.

##### Fixtures
Fixtures set up and provide necessary resources for the tests, ensuring a consistent and isolated testing environment.

```python
@pytest.fixture
def app():
```
- Sets up a Flask application instance with a test database. It creates the database tables, logs the registered routes, and cleans up by removing the database session and dropping all tables after tests are completed.
- Provides the Flask application instance for use in test functions.

```python
@pytest.fixture
def client(app):
```
- Provides a test client that simulates HTTP requests to the Flask application.
- Allows making requests and receiving responses during tests.

```python
@pytest.fixture
def auth_headers(app, client):
```
- Creates a test user, logs them in, and provides authorization headers with a Bearer token for authenticated requests.
- Supplies authorization headers with a Bearer token for making authorized requests in the tests.

```python
@pytest.fixture
def sample_user(app):
```
- Adds a sample user to the database if not already present for testing purposes.
- Returns the created user instance for use in the tests.

```python
@pytest.fixture
def sample_product(app):
```
- Adds a sample product to the database for testing order-related operations.
- Returns the created product instance for use in the tests.

```python
@pytest.fixture
def sample_cart(app, sample_user, sample_product):
```
- Creates a sample cart associated with the sample user and adds an item to it for testing.
- Returns the created cart instance for use in the tests.

##### Test Cases

```python
def test_place_order_with_empty_cart(client, auth_headers):
```
- Tests the behavior when attempting to place an order with an empty cart. Verifies that the correct error message is returned.
- Ensures the response status code is 400, and the message indicates that the cart is empty.

```python
def test_place_order_success(client, auth_headers, sample_cart):
```
- Tests placing an order successfully when the cart contains items. Verifies the order is placed, the cart is cleared, and the order ID is returned.
- Ensures the response status code is 201 and the order is placed with the correct ID. Confirms the cart is empty after placing the order.

```python
def test_get_order_history(client, auth_headers, sample_cart):
```
- Tests retrieving the order history for a user after placing an order. Verifies the order appears in the order history.
- Ensures the response status code is 200 and the order history contains the placed order, with the correct count of items in the order.

```python
def test_get_order_details(client, auth_headers, sample_cart):
```
- Tests retrieving the details of a specific order. Verifies that the correct order details, including the order ID and items, are returned.
- Ensures the response status code is 200 and the order details match the placed order.

```python
def test_get_nonexistent_order_details(client, auth_headers):
```
- Tests retrieving the details of a non-existent order. Verifies that the correct error message is returned when the order does not exist.
- Ensures the response status code is 404, and the message indicates that the order was not found.

#### `tests/test_products.py`

The `test_products.py` module provides unit tests for product-related API endpoints in the flask application. It ensures that operations like retrieving, adding, updating, and deleting products are working correctly.

##### Fixtures
Fixtures set up and provide necessary resources for the tests, ensuring a consistent and isolated testing environment.

```python
@pytest.fixture
def fixture_app():
```
- Sets up a Flask application instance with testing configurations and an in-memory SQLite database. It initializes extensions like JWT and registers product-related routes.
- Provides an admin user and a regular user for testing purposes.
- Cleans up by removing the database session and dropping all tables after tests are completed.

```python
@pytest.fixture
def fixture_client(fixture_app):
```
- Provides a test client that simulates HTTP requests to the Flask application.
- Allows making requests and receiving responses during tests.

```python
@pytest.fixture
def fixture_admin_jwt_token(fixture_app):
```
- Creates a JWT token for the admin user, which is used for authenticated admin requests during testing.
- Supplies the Bearer token for admin privileges.

```python
@pytest.fixture
def fixture_user_jwt_token(fixture_app):
```
- Creates a JWT token for the regular user, which is used for authenticated non-admin requests during testing.
- Supplies the Bearer token for regular user privileges.

```python
@pytest.fixture
def fixture_sample_product(fixture_app):
```
- Adds a sample product to the database for testing product-related operations.
- Returns the created product’s ID for use in the tests.

##### Test Cases

```python
def test_get_all_products(fixture_client, fixture_app, fixture_sample_product):
```
- Tests retrieving all products from the API. Verifies that the sample product added is present in the response.
- Ensures the response status code is 200, and the retrieved product list includes the sample product.

```python
def test_get_single_product(fixture_client, fixture_sample_product):
```
- Tests retrieving a single product by its ID. Verifies that the product details match the expected values.
- Ensures the response status code is 200, and the product details are correct.

```python
def test_get_nonexistent_product(fixture_client):
```
- Tests retrieving a product that doesn't exist. Verifies that a 404 error is returned.
- Ensures the response status code is 404, and the error message indicates the product was not found.

```python
def test_add_product_as_admin(fixture_client, fixture_admin_jwt_token):
```
- Tests adding a new product as an admin user. Verifies that the product is correctly added to the database and that the response confirms the addition.
- Ensures the response status code is 201, and the product is successfully added.

```python
def test_add_product_as_non_admin(fixture_client, fixture_user_jwt_token):
```
- Tests adding a new product as a non-admin user. Verifies that a 403 error is returned due to insufficient privileges.
- Ensures the response status code is 403, and the error message indicates admin privileges are required.

```python
def test_add_product_missing_fields(fixture_client, fixture_admin_jwt_token):
```
- Tests adding a new product with missing required fields (e.g., name and price). Verifies that a 400 error is returned.
- Ensures the response status code is 400, and the error message indicates the required fields are missing.

```python
def test_edit_product_as_admin(fixture_client, fixture_admin_jwt_token, fixture_sample_product):
```
- Tests editing an existing product as an admin user. Verifies that the product details are correctly updated.
- Ensures the response status code is 200, and the updated product details are applied.

```python
def test_edit_product_as_non_admin(fixture_client, fixture_user_jwt_token, fixture_sample_product):
```
- Tests editing an existing product as a non-admin user. Verifies that a 403 error is returned due to insufficient privileges.
- Ensures the response status code is 403, and the error message indicates admin privileges are required.

```python
def test_delete_product_as_admin(fixture_client, fixture_admin_jwt_token, fixture_sample_product):
```
- Tests deleting a product as an admin user. Verifies that the product is successfully removed from the database.
- Ensures the response status code is 200, and the product is deleted.

```python
def test_delete_product_as_non_admin(fixture_client, fixture_user_jwt_token, fixture_sample_product):
```
- Tests deleting a product as a non-admin user. Verifies that a 403 error is returned due to insufficient privileges.
- Ensures the response status code is 403, and the error message indicates admin privileges are required.

## Report on CartServiceProtocol Implementation and Bug Fixes

**associated requirements:**
- § NOTE: Consider discussing the use of Object-Oriented design, leveraging Python Protocols over inheritance (recommended) 

The cart functionality was initially implemented focusing on adding, removing, and viewing items in the shopping cart. 

Later, to meet one of the requirements, i created the `protocols.py` inside `app/`, and the `cart_service` in which the `SQLAlchemyCartService` class was created to handle database interactions using SQLAlchemy. A `ConcreteCartItem` class was also introduced to represent individual cart items, ensuring that each item had a `product_id` and `quantity` attribute.

The original `view_cart` method retrieves the cart data directly from the User model without using any abstraction or service layer. In this approach, all of the logic to access the user's cart and construct the response was embedded directly within the Flask route handler.

In the old approach, the `view_cart` function directly accessed the User model to fetch the user's cart, and then constructed a list of cart items with details such as product_id, name, quantity, and price. The logic for fetching and serializing the cart items was all inside the route handler:

```python
@cart_bp.route("", methods=["GET"])
@jwt_required()
def view_cart():
    """
    Retrieve the current user's cart.

    This endpoint fetches the items in the user's cart and returns them as a JSON object.

    Returns:
        JSON response with the cart items or an empty list if the cart does not exist.
    """
    user = User.query.get(get_jwt_identity())  # Directly querying the user and cart
    cart = user.cart
    if not cart:
        return jsonify({"cart": []}), 200
    
    # Serializing the cart items directly within the view function
    cart_items = [
        {
            "product_id": item.product_id,
            "name": item.product.name,
            "quantity": item.quantity,
            "price": item.product.price,
        }
        for item in cart.items
    ]
    
    return jsonify({"cart": cart_items}), 200
```

Here’s a view of how the get_cart method was structured:

```python
def get_cart(self, user_id: int) -> List[CartItem]:
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        return []
    return [
        ConcreteCartItem(product_id=item.product_id, quantity=item.quantity)
        for item in cart.items
    ]

```
This method correctly retrieved ConcreteCartItem objects for each item in the user's cart.

### Test Failure Encountered

While running the test for adding an item to the cart (test_add_to_cart), i encountered an error. Specifically, the test returned the following error message:

```python
-------------------------------------------------------------------------------- Captured log call --------------------------------------------------------------------------------
ERROR    app:error_handlers.py:48 An unhandled exception occurred: Object of type ConcreteCartItem is not JSON serializable
============================================================================= short test summary info =============================================================================
FAILED tests/test_carts.py::test_add_to_cart - KeyError: 'cart'
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
1 failed, 6 passed, 9 warnings in 1.56s
make: *** [Makefile:26: test] Error 1
```
The issue was that Flask's `jsonify` function couldn't serialize the `ConcreteCartItem` objects when returning the cart data via the /cart API. The test expected a JSON response containing the cart key with a list of cart items, but instead, Flask raised an error because `ConcreteCartItem` is not directly serializable to JSON.

To resolve the issue, i modified the view_cart method in `cart.py` to convert `ConcreteCartItem` objects into dictionaries (a format that is JSON serializable) before sending them in the API response. Below is the change i made to the `view_cart` function.

Before:

```python
return jsonify({"cart": cart_items}), 200
```
After:

```python
# Convert ConcreteCartItem objects to dictionaries for JSON serialization
serialized_cart_items = [
    {"product_id": item.product_id, "quantity": item.quantity}
    for item in cart_items
]

return jsonify({"cart": serialized_cart_items}), 200
```
This ensures that `ConcreteCartItem` objects are transformed into dictionaries, allowing Flask to properly serialize the response to JSON.

### Learnings

- One key learning is that custom Python objects cannot be directly serialized into JSON by Flask. We need to convert such objects into basic data types like dictionaries or lists before returning them as API responses.

- Running tests early in the development process allowed us to catch this issue before it made it into production. This highlights the importance of using unit tests to identify potential issues with serialization and other edge cases.

By separating the logic for retrieving cart items and serializing them into JSON format, we ensured the service class remained focused on database interactions while the API layer handled presentation logic (such as converting objects to a serializable format).

### Function `add_to_cart():`

```python
@cart_bp.route("", methods=["POST"])
@jwt_required()
def add_to_cart():
    """
    Add a product to the user's cart.

    This endpoint adds a product to the user's cart. If the cart does not exist, it will be created.
    If the product is already in the cart, its quantity will be updated.

    Returns:
        JSON response with a success message.
    """
    data = request.get_json()

    # Fetching user ID from JWT token
    user_id = get_jwt_identity()

    # Getting product_id and quantity from the request data
    product_id = data["product_id"]
    quantity = data.get("quantity", 1)  # Default to 1 if not provided

    # cart = user.cart
    # if not cart:
    #     cart = Cart(user_id=user.id)
    #     db.session.add(cart)
    #     db.session.commit()
    # product = Product.query.get_or_404(data["product_id"])
    # cart_item = CartItem.query.filter_by(
    #     cart_id=cart.id, product_id=product.id).first()
    # if cart_item:
    #     cart_item.quantity += data.get("quantity", 1)
    # else:
    #     cart_item = CartItem(
    #         cart_id=cart.id,
    #         product_id=product.id,
    #         quantity=data.get(
    #             "quantity",
    #             1))
    #     db.session.add(cart_item)
    # db.session.commit()

    # Delegating cart logic to the cart_service
    cart_service.add_item(
        user_id=user_id,
        product_id=product_id,
        quantity=quantity
    )
    return jsonify({"msg": "Product added to cart"}), 200
```
The `add_to_cart` function was directly manipulating the User, Product, and Cart models, which was causing tighter coupling and more complex logic in the route.

The function is now refactored to delegate the logic to cart_service, making the code more modular and easier to maintain. All cart-related business logic is now managed in the `cart_service`.


### Function `remove_from_cart(product_id):`

**Wrong Status Code When Removing a Non-Existent Item:**
- The `test_remove_nonexistent_item` test expected a 404 Not Found response, but the application returned a 200 OK response.
- The `remove_from_cart` method did not properly handle the case where the cart or cart item did not exist, leading to incorrect status codes.
- Error handling added to raise a `ValueError` in the `cart_service.remove_item()` method when the cart or item is not found. The remove_from_cart route catches the exception and returns a 404 Not Found.

Before:

```python
response = client.delete("/cart/999", headers=auth_headers)
assert response.status_code == 200  # Wrong expectation when item doesn't exist
```

After:

```python
@cart_bp.route("/<int:product_id>", methods=["DELETE"])
@jwt_required()
def remove_from_cart(product_id):
    try:
        cart_service.remove_item(user_id=user_id, product_id=product_id)
        return jsonify({"msg": "Item successfully removed from cart"}), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 404  # Return 404 if item is not found

```

**Incorrect Error Handling for Non-Existent Cart**

- The `remove_from_cart` method did not correctly handle the case where the user's cart did not exist, leading to failures.

```python
==================================================================================== FAILURES =====================================================================================
______________________________________________________________________________ test_remove_from_cart ______________________________________________________________________________

client = <FlaskClient <Flask 'app'>>
auth_headers = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyNjgzNTIxMSwianRpIjoiZTE...wZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzI2ODM1MjExLCJleHAiOjE3MjY4MzYxMTF9.4gtYw08NPr84VO3b64Q6fWkcllmZrq8B6nzHquEqrCU'}
sample_product = <Product 1>

    def test_remove_from_cart(client, auth_headers, sample_product):
        """
        Test removing a product from the cart.
    
        Adds a product to the cart and then removes it. Verifies that the product
        has been successfully removed and the cart is empty afterwards.
    
        Args:
            client (FlaskClient): The test client for the Flask application.
            auth_headers (dict): Authorization headers with the Bearer token.
            sample_product (Product): The sample product instance to remove from the cart.
        """
        # Adding product to cart
        client.post(
            "/cart",
            json={"product_id": sample_product.id, "quantity": 1},
            headers=auth_headers,
        )
    
        # Removing product from cart
        response = client.delete(
            f"/cart/{sample_product.id}",
            headers=auth_headers)
>       assert response.status_code == 200
E       assert 500 == 200
E        +  where 500 = <WrapperTestResponse streamed [500 INTERNAL SERVER ERROR]>.status_code

tests/test_carts.py:222: AssertionError
-------------------------------------------------------------------------------- Captured log call --------------------------------------------------------------------------------
ERROR    app:error_handlers.py:48 An unhandled exception occurred: type object 'CartItem' has no attribute 'query'
============================================================================= short test summary info =============================================================================
FAILED tests/test_carts.py::test_remove_from_cart - assert 500 == 200
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
1 failed, 7 passed, 8 warnings in 1.82s
make: *** [Makefile:26: test] Error 1

``` 
- The remove_item method did not raise an exception when the cart was not found, resulting in a 200 OK response even if the cart didn't exist.

- Updated the cart_service.remove_item() method to raise a ValueError if the cart is not found.

Before:

```python
cart = Cart.query.filter_by(user_id=user_id).first()
if cart:
    CartItemModel.query.filter_by(cart_id=cart.id, product_id=product_id).delete()
```

After:

```python
cart = Cart.query.filter_by(user_id=user_id).first()
if not cart:
    raise ValueError("Cart not found")  # Raise error if cart doesn't exist
```
### Summary

- Always ensure objects returned from a service are JSON serializable (e.g., converting to dictionaries).
Variable Initialization: Ensure that variables required by service methods are properly initialized and validated from request data.
- Use SQLAlchemy models for database queries and avoid using protocols or interfaces in database-related operations.
- Implement proper error handling for edge cases like non-existent items or carts. Use exceptions to communicate errors and return appropriate status codes.
- Keep business logic in service classes (e.g., SQLAlchemyCartService) and use controllers only for request handling and response formatting.

### Review on CartServiceProtocol Implementation

1. `cart_service.py` review:

The service provides methods for:

- `add_item`: Adds or updates an item in the cart.
- `remove_item`: Removes an item from the cart.
- `get_cart`: Retrieves all items from the user's cart.
- `clear_cart`: Removes all items from the cart.

These methods cover the basic functionality required to manage a shopping cart.

2. Implementation Review:

`add_item`:

- The method checks if the cart exists, creates it if necessary, and either updates the quantity of an existing item or adds a new item.
- Implementation: Fully implemented and integrated into add_to_cart in cart.py.

`remove_item`:

- The method checks for the cart's existence and removes a specific item if it is found. If either the cart or item is not found, it raises a `ValueError`.
- Implementation: Fully implemented and integrated into `remove_from_cart` in `cart.py`.

`get_cart`:

- The method retrieves all items from a user's cart and returns them as `ConcreteCartItem` instances.
- Implementation: Fully implemented and integrated into view_cart in `cart.py`.

`clear_cart`:

- The method removes all items from the user's cart.
- The method is implemented, but there is no Flask route (`cart.py`) currently using it. 


```python
@cart_bp.route("/clear", methods=["DELETE"])
@jwt_required()
def clear_cart():
    """
    Clear the user's entire cart.
    """
    user_id = get_jwt_identity()
    cart_service.clear_cart(user_id)
    return jsonify({"msg": "Cart cleared"}), 200
`` 
New test:

```python
def test_clear_cart(client, auth_headers, sample_product):
    """
    Test clearing the cart.
    
    This test ensures that the entire cart is cleared when calling the clear_cart endpoint.
    It first adds a product to the cart, then calls the clear endpoint and verifies that the cart is empty.
    """
    # Add a product to the cart
    client.post(
        "/cart",
        json={"product_id": sample_product.id, "quantity": 1},
        headers=auth_headers,
    )

    # Verify the cart is not empty
    response = client.get("/cart", headers=auth_headers)
    data = json.loads(response.data)
    assert len(data["cart"]) == 1

    # Clear the cart
    response = client.delete("/cart/clear", headers=auth_headers)
    assert response.status_code == 200
    assert json.loads(response.data)["msg"] == "Cart cleared"

    # Verify the cart is empty
    response = client.get("/cart", headers=auth_headers)
    data = json.loads(response.data)
    assert data["cart"] == []
```

----
## Summary of Learnings and Challenges

- Initially, some challenges were faced with route duplication and improper structuring. This was resolved by properly organizing routes into blueprints and ensuring consistent URL prefixes.

- Implementing JWT authentication required careful consideration of token generation and validation processes.

- Learned the importance of creating and applying database migrations when making model changes, even when the changes seemed minor.

- Implementing comprehensive error handling across the application was important for providing meaningful feedback to API consumers.

- Developing a robust testing strategy, including unit tests for critical functions and integration tests for API endpoints, was essential for ensuring reliability.

## Approach and Design Decisions

- Utilized OOP principles in structuring the models and service layers, allowing for clean separation of concerns and easier maintainability.

- Flask blueprints were used to organize routes logically, improving code structure and allowing for modular development.

- Implemented an ORM for database operations, abstracting data access logic and making it easier to switch databases if needed in the future.

### Factory Pattern

[Factory Method Pattern](https://en.wikipedia.org/wiki/Factory_method_pattern)

Used the Factory Pattern in creating the Flask application, allowing for easy configuration of different environments (development, testing, production).

```python
def create_app(config_class=Config) -> Flask:
    """
    Creates and configures an instance of the Flask application.

    Args:
        config_class (Type[ConfigType]): The configuration class to use for the application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)
    Migrate(app, db)

    # Register blueprints
    app.register_blueprint(cart_bp)
    app.register_blueprint(routes_bp)
    app.register_blueprint(orders_bp)

    # Register global error handlers
    register_error_handlers(app)

    return app
```

- The `create_app` function serves as the `factory` method for creating Flask application instances.
- It takes a `config_class` parameter, which allows for different configurations to be passed in (e.g., development, testing, production). This flexibility is a key benefit of the Factory Pattern.
- The function **creates a new Flask application instance, configures it based on the provided configuration class, initializes extensions (database, JWT, migrations), registers blueprints, and sets up error handlers.**
- Finally, it returns the fully configured Flask application instance.

This implementation allows for easy creation of differently configured application instances, which is particularly useful for:

- Creating separate instances for development, testing, and production environments.
- Facilitating unit testing by allowing the creation of test-specific application instances.
- Enabling modular development by centralizing the application setup process.

The use of this pattern is evident in various parts of the project, such as in the test files where different configurations are used to create test-specific application instances. For example, in `tests/test_auth.py`:

```python
@pytest.fixture
def app():
    """
    Fixture for creating and configuring the Flask application.

    Sets up the application context and creates the database tables
    before yielding the app instance. After tests complete, it removes
    the database session and drops all tables to clean up.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = create_app(TestConfig)
    with app.app_context():
        logger.debug("Creating database tables")
        db.create_all()
        logger.debug("Database tables created")
        yield app
        logger.debug("Removing database session")
        db.session.remove()
        logger.debug("Dropping all tables")
        db.drop_all()
        logger.debug("All tables dropped")
```

Dependency Injection is primarily applied through the use of Flask extensions and the application context, although it's not explicitly implemented.

- The `SQLAlchemy` and `JWTManager` instances are created separately in `extensions.py` and then initialized with the app in `create_app()`. This is a form of dependency injection where these dependencies are "injected" into the app rather than created within it.

- Flask's application context allows dependencies like `db` to be accessed throughout the application without explicitly passing them around. This is a form of implicit dependency injection.

- Functions like `get_jwt_identity()` and `verify_jwt_in_request()` are used in route handlers, injecting JWT functionality without tightly coupling it to the route logic.

- The `db` object is imported and used in route handlers and models, allowing database operations without creating new database connections in each function.

### Python Protocols

- Leveraged for defining clear interfaces, especially in service layers, promoting loose coupling and easier mocking in tests.

### RESTful API Design

- Adhered to REST principles in designing API endpoints for consistent and intuitive interaction.

## Challenges and Solutions

- Initial route setup led to conflicts and duplications. The solution was to reorganize routes using blueprints and consistent URL prefixing.

- Issues with JWT token validation in certain routes were resolved by implementing consistent JWT decorators and error handling across all protected routes.

- Ensuring test isolation was crucial to prevent tests from affecting the global state or each other. To achieve this, specific fixtures were created for managing user sessions, product data, and authentication headers.

- Tests were made efficient and clean. The use of fixtures to initialize common components (e.g., a sample user, a sample product) made the test code DRY (Don't Repeat Yourself) and ensured efficient resource management by leveraging scoped sessions.

- One of the challenges encountered was dealing with `sqlalchemy.orm.exc.DetachedInstanceError`. This taught the importance of managing SQLAlchemy session scope and how to refresh and bind instances correctly to avoid errors related to detached objects during testing.

- Managing SQLAlchemy sessions within tests required careful use of `db.session.remove()` and `db.drop_all()` to ensure test isolation. The trade-off was a slight increase in the complexity of fixture design, but this ensured that the tests were isolated and reliable.

- Pylint was an important tool for enforcing coding standards, but it required some customization. For instance, the default order of imports and handling of unused variables led to disabling certain checks in specific test scenarios. The trade-off was allowing some violations (like long lines or unused variables in test fixtures) to improve code readability and focus on testing functionality.

- In Python, protocols (introduced in PEP 544) allow us to specify "structural subtyping" without inheritance. However, given that SQLAlchemy relies on classical inheritance for ORM mappings, the project used inheritance in models like `User`, `Cart`, and `Order`. Later on, protocols were leveraged to decouple concrete implementations and enforce contracts between services, like the cart service. The use of protocols was limited to the cart service due to time constraints, but this approach demonstrates the potential for wider application in future development.

### Assumptions Made

- It was assumed that a robust testing environment would need to be set up, including Flask application fixtures, database setup and teardown, and test client configurations. The focus was on ensuring a clean state between tests by dropping and recreating the database tables for each test module.

- The solution assumes the need for thorough error handling across the application. This includes ensuring appropriate HTTP status codes (e.g., 400 for invalid requests, 404 for not found resources, and 500 for server errors) and meaningful error messages.

### Errors and Mistakes

- Early tests failed because the necessary tables were not being created in the test environment. This was a critical oversight in understanding how Flask and SQLAlchemy manage test environments.

- The `db` fixture was mistakenly assumed to be automatically available in PyTest. However, it needed to be defined or appropriately imported for test cases that required database interaction.

#### More Errors

When accessing a `Product` outside of a database session, SQLAlchemy raised a `DetachedInstanceError`. This mistake highlighted the need to ensure that objects are always tied to an active session when accessed or modified.

- In one iteration, routes weren’t being properly registered, which led to 404 errors in tests. This was solved by ensuring that blueprints and all routes were correctly registered within the application context.

- Tests were failing due to conflicts between fixtures in different test files, particularly with the `app` fixture.

- Proper scoping of fixtures is important. Use `scope="module"` for fixtures that should be shared across all tests in a file.

- Be mindful of the database state between tests. Consider using transactions or database cleaning strategies to ensure a clean slate for each test.

Encountered `IntegrityError: UNIQUE constraint failed: user.email` when trying to create test users.

- Always check for existing records before inserting new ones, especially in test setups.

- Use `get_or_create` patterns in fixtures that set up test data.

- Consider using unique identifiers (e.g., timestamps) in test data to avoid conflicts.

Detached instance errors occurred when trying to access model attributes outside of database sessions.

- Always access and modify database objects within an active session context.

- Be cautious when passing database objects between functions or storing them for later use.

- Use `db.session.merge()` or re-query objects if you need to work with them in a new session.

Initially, there were issues with different configurations for development and testing environments.

- Create separate configuration classes for different environments (development, testing, production).

- Use environment variables for sensitive or environment-specific configurations.

- Ensure that the test configuration uses a separate database (preferably in-memory) from the development environment.

Initial implementation didn't properly separate authentication from authorization.

- Clearly distinguish between authentication (verifying who a user is) and authorization (what they're allowed to do).

- Implement proper middleware or decorators for checking user roles and permissions.

- Use JWT tokens correctly, ensuring they carry necessary claims for authorization checks.

Initially, error responses were inconsistent across different endpoints.

- Implement a global error handler to ensure consistent error responses across the API.

- Use custom exception classes for different types of application errors.

- Always include helpful error messages and appropriate HTTP status codes in error responses.

Initial test suite didn't cover all edge cases and error scenarios.

- Strive for comprehensive test coverage, including happy paths, edge cases, and error scenarios.

- Use parameterized tests to cover multiple scenarios efficiently.

- Regularly run coverage reports to identify untested parts of the code.

The Makefile had a "missing separator" error, which is typically caused by incorrect indentation.

- Makefiles require tabs for indentation, not spaces.

- Each command in a Makefile rule must start with a tab character.

- Be cautious when copying Makefile content from sources that might convert tabs to spaces.

- Configure your text editor to use actual tabs for Makefiles.

The initial approach included git configuration commands directly in the Makefile.

- Git configuration in Makefiles can be problematic in CI/CD environments.

- Consider setting git configurations at the CI/CD level rather than in the Makefile.

- If git operations are necessary in the Makefile, ensure the CI environment has the proper permissions and configurations.

#### More Errors

- Registered the `orders_bp` blueprint multiple times with different URL prefixes (`/api` and `/orders`), resulting in duplicate routes being generated for the order-related endpoints.

- The cart-related routes had the `/api` prefix, while other routes did not. This inconsistency can lead to confusion and make it harder to maintain and consume the API.

- After changing the route URLs, didn't immediately update the corresponding URLs in the unit tests, causing the tests to fail.

- Not adding the `.env` file to `.gitignore` early in the development phase.