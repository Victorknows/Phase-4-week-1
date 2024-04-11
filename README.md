# Pizza Restaurant API

# This is a simple RESTful API built with Flask to manage pizza restaurants and their pizzas.
# It allows you to perform CRUD operations on restaurants and pizzas, as well as associate pizzas with restaurants and set their prices.

## Installation

# 1. Make sure you have Python installed. You can download it from python.org.

# 2. Clone this repository:
#    ```bash
#    git clone https://github.com/your_username/pizza-restaurant-api.git
#    ```

# 3. Navigate to the project directory:
#    ```bash
#    cd pizza-restaurant-api
#    ```

# 4. Install the required dependencies:
#    ```bash
#    pip install -r requirements.txt
#    ```

## Usage

# 1. Run the Flask application:
#    ```bash
#    python app.py
#    ```

# 2. The API will be accessible at `http://localhost:5000`.

# 3. Use tools like cURL, Postman, or your preferred HTTP client to interact with the API. Refer to the API routes listed below.

## API Routes

### Restaurants

# - `GET /restaurants`: Retrieve all restaurants.
# - `GET /restaurants/<int:id>`: Retrieve a specific restaurant by ID.
# - `POST /restaurants`: Create a new restaurant.
# - `DELETE /restaurants/<int:id>`: Delete a restaurant by ID.

### Pizzas

# - `GET /pizzas`: Retrieve all pizzas.
# - `POST /pizzas`: Create a new pizza.

### Restaurant Pizzas

# - `POST /restaurant_pizzas`: Associate a pizza with a restaurant and set its price.

## Database

# The application uses SQLite as the database, with a single file named `pizza.db`.
# You can modify the database configuration in `app.py` if needed.

# AUTHOR
Victor Muhoro

## Contributing

# Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

# [MIT](https://choosealicense.com/licenses/mit/)
