# ecommerce-flask-backend
---

## Assignment 
---
**Problem Statement:**

Create a backend system for a simple e-commerce platform where users can register, view a list of products, add products to a cart, and place an order. You should also implement basic user authentication and ensure that users can only view and manipulate their own data.

**Requirements:**

• **User Management:**
  - The persona for Users should be able to register, log in, and manage their account.
  - Passwords should be securely stored (e.g., hashed).

• **Product Management:**
  - The persona for Admins should be able to add, edit, and remove products.
  - Regular users should be able to view a list of products and details of each product.

• **Cart and Order Management:**
  - Users should be able to add products to a cart.
  - Users should be able to view their cart and place an order.
  - Once an order is placed, the cart should be cleared, and the order details should be saved.

• **Data Persistence:**
  - Store user, product, cart, and order data in a file-based database (e.g., JSON, SQLite).

• **Testing:**
  - Write basic unit tests for persona critical functions like user registration, product addition, and order placement.

• **Error Handling:**
  - Handle common errors such as invalid inputs, unauthorized access, and unavailable products.

• **Version Control:**
  - Use Git to manage your project. Make regular commits and document your work in a README file.

**Tested Competencies:**

• **Problem-Solving Skills:**
  - The challenge requires designing and implementing a solution that involves multiple components (users, products, orders), testing the candidate’s ability to break down complex problems using Software Engineering best practices.

• **Programming Fundamentals:**
  - The candidate will need to use object-oriented design, design patterns, basic data structures (e.g., lists, dictionaries), control flow, and functions to manage the application’s logic.

• **Code Quality:**
  - The candidate’s ability to write clean, readable code is tested by the need to organize different components of the application, adhere to DRY (Don't Repeat Yourself) principles, and provide comments where necessary indicating input parameters, return, and ensuring function signatures contain variable annotations.

• **Testing and Debugging:**
  - Writing unit tests for key functions assesses testing skills, while debugging the implementation is necessary to ensure the application works as expected. TDD is validated and preferred by reviewing the commit history.

• **Language Proficiency:**
  - Demonstration of Python proficiency by implementing the application with correct syntax, using appropriate libraries, and following best practices (e.g., comments, variable annotations, list comprehensions, etc.).

• **Version Control:**
  - Use of Git can be assessed by reviewing the solution’s commit history indicating branch management and overall use of basic version control.

• **Communication Skills:**
  - Explaining the solution approach in the well-formatted README.md documents their implementation and should describe any assumptions made. (Often problems are not well-formed and require a bit of decision-making. Use this as an opportunity to show how well you identify missing or incomplete information and press forward with a solution that is under test.)

• **Adaptability and Learning:**
  - If unfamiliar with certain aspects (like user authentication or writing tests), use the README.md to identify areas you had to look up to learn on the fly as a demonstration of the ability to adapt.

**Challenge Instructions:**

• Anticipated Time Required: Less than 4 hours

• Tools Required: Python, the IDE of your choosing, internet access, and git.

• Deliverables:
  1. The codebase in a compressed file containing the entire git repository.
     § NOTE: Be sure to include the .git file for inspection of commits.
  2. A README.md file containing at a minimum a general project description, how to set up and run the application, how to test the application, any assumptions made, and any learnings you had to do to design and/or implement the solution.
  3. A description of the approach taken and any trade-offs or decisions made during implementation.
     § NOTE: Consider discussing the use of Object-Oriented design, leveraging Python Protocols over inheritance (recommended), Design Patterns (see here for an overview of design patterns), and anything you believe would be a good callout for this challenge illustrating your programming, systems thinking, and general expertise.

**Rubric:**

Your code submission will be assessed based on the quality of the solution in addressing the 8 competencies identified above in the “Tested Competencies” section.

--- 

Se precisar de mais alguma coisa ou de outra formatação específica, é só avisar!

## Project Structure

```
ecommerce-backend/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── products.py
│   │   ├── cart.py
│   │   └── orders.py
│   ├── schemas.py
│   └── utils.py
├── tests/
│   ├── test_auth.py
│   ├── test_products.py
│   ├── test_cart.py
│   └── test_orders.py
├── migrations/
├── .gitignore
├── requirements.txt
├── config.py
├── run.py
└── README.md
```

## Stack
Language: Python
Web Framework: Flask
Database: SQLite
Auth:
ORM: SQLAlchemy
Testing: pytest
Version control: Github

## Files
### app/models.py
This file defines the database schema for a simple e-commerce backend using SQLAlchemy, an Object-Relational Mapping (ORM) library for Python. Let's break down each model and its components:

1. User Model:
   - Represents registered users of the e-commerce platform.
   - Fields:
     - id: Unique identifier for each user
     - username: User's chosen username (unique)
     - email: User's email address (unique)
     - password_hash: Hashed version of the user's password for security
     - is_admin: Boolean flag to identify admin users
   - Relationships:
     - cart: One-to-one relationship with the Cart model
     - orders: One-to-many relationship with the Order model
   - Methods:
     - set_password: Hashes and sets the user's password
     - check_password: Verifies a given password against the stored hash

2. Product Model:
   - Represents products available in the e-commerce platform.
   - Fields:
     - id: Unique identifier for each product
     - name: Name of the product
     - description: Detailed description of the product
     - price: Price of the product
     - stock: Current stock quantity of the product

3. Cart Model:
   - Represents a user's shopping cart.
   - Fields:
     - id: Unique identifier for each cart
     - user_id: Foreign key linking to the User model
   - Relationships:
     - items: One-to-many relationship with the CartItem model

4. CartItem Model:
   - Represents individual items in a user's cart.
   - Fields:
     - id: Unique identifier for each cart item
     - cart_id: Foreign key linking to the Cart model
     - product_id: Foreign key linking to the Product model
     - quantity: Quantity of the product in the cart
   - Relationships:
     - product: Many-to-one relationship with the Product model

5. Order Model:
   - Represents a completed order.
   - Fields:
     - id: Unique identifier for each order
     - user_id: Foreign key linking to the User model
     - total: Total price of the order
   - Relationships:
     - order_items: One-to-many relationship with the OrderItem model

6. OrderItem Model:
   - Represents individual items in a completed order.
   - Fields:
     - id: Unique identifier for each order item
     - order_id: Foreign key linking to the Order model
     - product_id: Foreign key linking to the Product model
     - quantity: Quantity of the product in the order
     - price: Price of the product at the time of order (in case product prices change later)
   - Relationships:
     - product: Many-to-one relationship with the Product model

This schema allows for:
- User registration and authentication
- Product management
- Shopping cart functionality
- Order placement and history

The relationships between these models enable efficient querying and data management. For example, we can easily retrieve all items in a user's cart or all orders placed by a user.
