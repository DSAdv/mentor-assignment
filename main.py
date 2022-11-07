from app import create_app
from flask.cli import with_appcontext
from models import db

app = create_app()


@app.cli.command()
@with_appcontext
def init_db():
    """Initialize the database with required tables."""
    db.create_all()


def main():
    app.run(port=5000, debug=True)


if __name__ == '__main__':
    main()
