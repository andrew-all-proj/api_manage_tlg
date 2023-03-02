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
        except Exception as ex:
            db.session.rollback()
            return False

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as ex:
            print(ex)
            return False

    def to_archive(self):
        self.is_archive = True

    def id_split(self, id):
        if (not id): return id
        return "".join(str(id).split()) or id
