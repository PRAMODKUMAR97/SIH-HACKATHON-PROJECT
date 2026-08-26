"""Start KHANAN-NETRA in local DEMO DATA mode."""
import webbrowser
from threading import Timer
import uvicorn

if __name__ == "__main__":
    print("KHANAN-NETRA DEMO DATA starting at http://127.0.0.1:8000")
    Timer(1.2, lambda: webbrowser.open("http://127.0.0.1:8000")).start()
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=False)
