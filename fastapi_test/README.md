install if needed (installed at $HOME/.local/bin):

``pip install "uvicorn[standard]" gunicorn``


run with:

``uvicorn main:app --host 0.0.0.0 --port 8000``

or as deamon:

``gunicorn main:app -D --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000``


