# DB_CONFIG = {
    
#     "host": "localhost",
#     "user": "root",
#     "password": "", # change accordingly
#     "database": "microservices_dashboard", # change accordingly
#     "DATABASE_URL": "mysql+pymysql://root:@localhost/microservices_dashboard"

# }

import os
from dotenv import load_dotenv

# Load environment variables from a .env file (optional)
load_dotenv()

class Settings:
    PROJECT_NAME: str = "DataVizHub"
    PROJECT_VERSION: str = "1.0.0"

    # Database Configuration
    DB_USER: str = os.getenv("DB_USER", "root")  # Default XAMPP MySQL user
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")  # No password by default
    DB_HOST: str = os.getenv("DB_HOST", "localhost")  # XAMPP runs on localhost
    DB_PORT: str = os.getenv("DB_PORT", "3306")  # Default MySQL port
    DB_NAME: str = os.getenv("DB_NAME", "microservices_dashboard")

    DATABASE_URL: str = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Other Configurations
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

settings = Settings()
