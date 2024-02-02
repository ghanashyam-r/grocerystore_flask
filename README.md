The Flask-based multi-user e-commerce app facilitates grocery shopping with efficient product management. The store manager can add categories and items with unique IDs, names,quantity and details such as expiry date and prices.Users can browse and purchase groceries, add items to their cart, and proceed to checkout.
It ensures a seamless shopping experience for customers across different categories.

Video Demo:
https://www.linkedin.com/posts/ghanashyam-r-_flask-webdevelopment-mad1course-activity-7112738720822284288-GMiU?utm_source=share&utm_medium=member_desktop

Technologies used:
    Flask: A micro web framework used to build the backend of the application.
    Flask-SQLAlchemy: Object-Relational Mapping (ORM) tool for interacting with the database and allows easy integration with the Flask application.
    Flask-Login: Extension for user authentication and session management
    SQLite: Relational database used for storing product, section,
    HTML, Jinja2 templates, Bootstrap: Frontend technologies for user interface design

DB Schema Design
    PK-Primary Key,Fk-Foreign Key
    
    User Table:
    Columns: id (PK), username, email, is_admin, password_hash. Constraints: Unique combination of username and email.
    Relationships:
    One-to-many with Item (owned items). One-to-many with Cart (items in the cart).
    
    Item Table:
    Columns: id (PK), name, expdate, quantity, price, owner (FK), category_id (FK). Constraints: Unique combination of name and owner.
    Relationships:
    Many-to-one with User (owner). Many-to-one with Category (item category). One-to-many with Cart (cart items).
    
    Cart Table:
    Columns: id (PK), user_id (FK), item_id (FK), quantity.
    Relationships: Many-to-one with User. Many-to-one with Item.
    
    Category Table: Columns: id (PK), name.
    ● Foreign key constraints ensure data integrity by linking related tables.
    ● Relationships between models facilitate easy querying and accessing related data.
    ● Utilizes Flask-Login UserMixin for user authentication.
    ● Supports adding products to carts and placing orders with one-to-one and one-to-many
    relationships.

    
The project follows the MVC (Model-View-Controller) pattern. 
Controllers are responsible for handling user requests, views are responsible for rendering templates, and models define the database structure.
The routes.py is used for navigation.The models.py file contains the database models using SQLAlchemy. 
The templates folder contains the HTML templates for rendering the frontend.
Features implemented include:
  ● Multi-user authentication. Admin and multi-user login and sign up
  ● Inventory and Product Management: Admin can add, edit, and delete items and categories
  ● Order Processing: Search for sections and buy products from one or multiple sections

<img width="1437" alt="Screenshot 2024-02-02 at 10 29 25 PM" src="https://github.com/ghanashyam-r/grocerystore_flask/assets/138144872/f4918784-dca3-4eea-88eb-9660b7a5bd1b">
<img width="1438" alt="Screenshot 2024-02-02 at 10 30 30 PM" src="https://github.com/ghanashyam-r/grocerystore_flask/assets/138144872/5727565b-3f82-4f82-92dc-b06c143409a3">


    
