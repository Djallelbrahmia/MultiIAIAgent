import subprocess
import threading
import time
from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from dotenv import load_dotenv
logger = get_logger(__name__)

load_dotenv()

def run_backend():
    try:
        logger.info("Starting backend server...")
        subprocess.run(["uvicorn", "app.backend.api:app", "--host", "127.0.0.1", "--port", "9999"],check=True)
    except Exception as e: 
        logger.error("Failed to start backend server")
        raise CustomException("Backend server failed to start",e) 
    
def run_frontend():
    try:
        logger.info("Starting frontend server...")
        subprocess.run(["streamlit", "run", "app/frontend/ui.py"],check=True)
    except Exception as e:
        logger.error("Failed to start frontend server")
        raise CustomException("Frontend server failed to start")
    
if __name__ == "__main__":
    try:
        backend_thread = threading.Thread(target=run_backend)
        frontend_thread = threading.Thread(target=run_frontend)

        backend_thread.start()
        time.sleep(5) 
        frontend_thread.start()

    except Exception as e:
        logger.error("Failed to start application")
        raise CustomException("Application failed to start")