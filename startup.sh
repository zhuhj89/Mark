nohup gunicorn -w 4 -b 218.241.108.63:8080  run:mark_app >>app.log &
