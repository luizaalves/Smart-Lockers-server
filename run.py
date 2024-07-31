from app import create_app

app = create_app()

import os

print(f"Starting server with PID: {os.getpid()}")

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)