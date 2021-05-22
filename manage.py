from flask_script import Manager

import config
from app import create_app

app = create_app()
app.config.from_object(config.Config)
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
