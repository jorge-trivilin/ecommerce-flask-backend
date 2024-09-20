import os
import logging
from dotenv import load_dotenv
from app import create_app
from flask import jsonify

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()

app = create_app()

@app.route('/')
def index():
    return """
    <h1>E-commerce API</h1>
    <ul>
        <li>/auth/register - Register a new user</li>
        <li>/auth/login - Login user</li>
        <li>/products - List all products</li>
        <li>/cart - View cart</li>
        <li>/orders - Place an order</li>
        <li><a href="/routes">/routes - List all routes</a></li>
    </ul>
    """

@app.route('/routes')
def list_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            "endpoint": rule.endpoint,
            "methods": list(rule.methods), # type: ignore
            "path": str(rule)
        })
    return jsonify(routes)

def log_routes(app):
    logger.info("Registered routes:")
    for rule in app.url_map.iter_rules():
        logger.info(f"{rule.endpoint}: {rule.rule}")

if __name__ == "__main__":
    log_routes(app)
    debug_mode = os.getenv("FLASK_ENV") == "development"
    logger.info(
        f"Starting application in {'debug' if debug_mode else 'production'} mode"
    )
    app.run(debug=debug_mode)

# http://localhost:5000/products