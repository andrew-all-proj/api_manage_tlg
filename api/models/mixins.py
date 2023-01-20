from sqlalchemy.exc import IntegrityError
from api import db


class ModelDbExt:
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except IntegrityError:  # Обработка ошибки "создание пользователя с НЕ уникальным именем"
            db.session.rollback()
            return False

""" def delete(self):
        db.session.delete(self)
        db.session.commit()"""