import uvicorn
import os
import sys

# Ensure backend package is in python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

if __name__ == "__main__":
    print("[KHANAN-NETRA] Starting Core Intelligence & Backend Server...")
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)
