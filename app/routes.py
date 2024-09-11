from app import app


@app.route('/')
@app.route('/index')
def index():
    return "<h1>Welcome to DigiShop</h1><h2>Sign in to get started</h2>"
