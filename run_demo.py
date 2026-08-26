"""One-command, local KHANAN-NETRA offline demonstration launcher."""
import webbrowser
from threading import Timer

import uvicorn


def main() -> None:
    print("KHANAN-NETRA is starting in OFFLINE DEMO MODE at http://127.0.0.1:8000")
    Timer(1.2, lambda: webbrowser.open("http://127.0.0.1:8000")).start()
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=False)


if __name__ == "__main__":
    main()
