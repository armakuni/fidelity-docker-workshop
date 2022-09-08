import os
import time
import redis
from flask import Flask 

app = Flask(__name__)
cache = redis.Redis(
    host=os.environ.get('REDIS_HOST', 'localhost'), 
    port=os.environ.get('REDIS_PORT', '6379')
)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr("hits")
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route("/")
def hello():
    count = get_hit_count()
    return "Hello World! I have been seen {} times.\n".format(count)

if __name__ == "__main__":
    app.run(
        host=os.environ.get('FLASK_HOST', '0.0.0.0'), 
        port=os.environ.get('FLASK_PORT', 5000)
    )