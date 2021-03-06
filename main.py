"""
Quart development server with automatic restarts.
"""

import time
import traceback


def run():
    while True:
        try:
            from app.views import app
        except Exception:
            traceback.print_exc()
            print()
            time.sleep(3)
        else:
            app.run(host="0.0.0.0", debug=True)
            break


if __name__ == "__main__":
    run()
