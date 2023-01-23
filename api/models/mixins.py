from sqlalchemy.exc import IntegrityError
from api import db


class ModelDbExt:
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as ex: #IntegrityError:  # Обработка ошибки "создание пользователя с НЕ уникальным именем"
            db.session.rollback()
            print(ex)
            return False

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as ex:
            print(ex)
            return False