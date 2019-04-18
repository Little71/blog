import os

from flask_migrate import Migrate

from app import create_app
from app.models.base import db
from app.models import user, role

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
print(app.debug)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=user.User, Role=role.Role)


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    app.run()