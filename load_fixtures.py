import click
import json

from api import app
from api.models.channels_model import ChannelModel, UserChannelModel
from api.models.events_model import EventModel
from api.models.media_contents_model import TypeMediaModel, MediaContentModel
from api.models.media_tags_model import TagModel
from api.models.posts_model import PostsModel, media
from api.models.users_model import UserModel
from config import BASE_DIR
from sqlalchemy.exc import IntegrityError


@click.command
@click.option('--fixture', help='fixture name .json')
def load_fixture(fixture):
    app.app_context().push()
    path_to_fixture = BASE_DIR / "fixtures" / fixture
    models = {
        "UserModel": UserModel,
        "ChannelModel": ChannelModel,
        "EventModel": EventModel,
        "PostsModel": PostsModel,
        "TagModel": TagModel,
        "TypeMediaModel": TypeMediaModel,
        "UserChannelModel": UserChannelModel,
        "MediaContentModel": MediaContentModel,
        "media": media #добавить метод для связывания
    }
    coun = 0
    with open(path_to_fixture, "r", encoding="UTF-8") as f:
        data = json.load(f)
        model_name = data["model"]
        model = models[model_name]
        for record in data["records"]:
            model_object = model(**record)
            result = model_object.save()
            if result:
                coun=coun + 1
    print(f"add {coun}")


if __name__ == "__main__":
    load_fixture()