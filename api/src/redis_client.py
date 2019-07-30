from flask_redis import FlaskRedis


def create_client(flask_app):
    flask_app.config['REDIS_URL'] = "redis://redis:6379/0"
    return FlaskRedis(flask_app)
