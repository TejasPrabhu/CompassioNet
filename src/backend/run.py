import os
from backend import create_app
from backend.config import DevelopmentConfig, ProductionConfig


if os.getenv("FLASK_ENV") == "production":
    app = create_app(ProductionConfig)
else:
    app = create_app(DevelopmentConfig)

if __name__ == "__main__":
    app.run()
