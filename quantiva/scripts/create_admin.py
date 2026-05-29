import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..'
        )
    )
)

from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():

    user_exists = User.query.filter_by(
        username='admin'
    ).first()

    if not user_exists:

        admin = User(
            username='admin',
            email='admin@quantiva.com'
        )

        admin.set_password('123456')

        db.session.add(admin)
        db.session.commit()

        print("Administrador creado")

    else:

        print("El usuario ya existe")