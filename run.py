import os
import logging
from dotenv import load_dotenv
from app import create_app

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()

app = create_app()


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
