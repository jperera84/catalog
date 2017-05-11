# Catalog Project

The project is a FLASK Web Application for the Fullstack Web Foundation Module of the Nanodegree.

## Configuration and deploy

1. Create the database (Optional if use the catalog.db file provided is used)
    - run the command: ```python database_setup.py```
    This run all the database setup to create the tables in the database.
2. Run the seed data (Optional if use the catalog.db file provided is used)
    - run the command: ```python database_seed.py```
    This create the Categories that will be show in the Catalog
3. Run the application
    - run the command: ```python app.py```
    This will initialize the server application.

## Test the Application

Enter in your browser the following url: [http://localhost:5001/](http://localhost:5001/)

## Features

1. List of Categories and the latest 10 Items that were created.
2. Users can clic on the categories name to list all the items by category.
3. Users can login with their Google Account.
4. After Login:
    - Users can Add a new item.
    - Edit its own items.
    - Delete its own items.


## General Comments

1. In the database table exists some attributes that are not being use in this version of the application, they were added for future enhancements.

