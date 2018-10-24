from store_app import create_app
from Instance.config import Config

app = create_app(Config)
app_context = app.app_context()
app_context.push()

if __name__ == '__main__':
    app.run()