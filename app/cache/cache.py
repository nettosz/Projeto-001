from flask_caching import Cache

cache = Cache(config={'CACHE_TYPE': 'simple'})

def configure(app):
    cache.init_app(app)
    