from .utils.db import DB
from marshmallow import Schema, fields, validate

class MoodSchema(Schema):
    seed_artists = fields.List(fields.String(), validate=validate.Length(min=1))
    seed_genres = fields.List(fields.String(), validate=validate.Length(min=1))
    seed_tracks = fields.List(fields.String(), validate=validate.Length(min=1))
    
    # each is num list [min, max, target]
    # TODO: check if min < target < max
    danceability = fields.List(fields.Number(), validate=validate.Length(equal=3))
    instrumentalness = fields.List(fields.Number(), validate=validate.Length(equal=3))
    popularity = fields.List(fields.Number(), validate=validate.Length(equal=3))
    speechiness = fields.List(fields.Number(), validate=validate.Length(equal=3))
    valence = fields.List(fields.Number(), validate=validate.Length(equal=3))
    energy = fields.List(fields.Number(), validate=validate.Length(equal=3))


class Mood:
    def __init__(self, name, creator_id, params, mood_id):
        self.name = name
        self.creator_id = creator_id
        self.params = params
        self.mood_id = mood_id
    

class MoodGenerator:
    def __init__(self, name, creator_id, params, mood_id, strategy):
        self.name = name
        self.creator_id = creator_id
        self.params = params
        self.strategy = strategy
        self.mood_id = mood_id

    def set_strategy(self, strategy):
        self.strategy = strategy

    def generate(self):
        return self.strategy(self.name, self.creator_id, self.params, self.mood_id).generate()


class GenerationStrategy:
    def __init__(self, name, creator_id, params, mood_id):
        self.name = name
        self.creator_id = creator_id
        self.params = params
        self.mood_id = mood_id
    
    def generate(self):
        raise NotImplementedError


class CreateOrUpdateMoodStrategy(GenerationStrategy):
    def generate(self):
        deserialized = MoodSchema().loads(\
                {} if self.params is None else self.params)
        mood_id = None
        with DB() as db:
            mood_id, _ = db.get_mood_by_name(self.name, self.creator_id)
            create_or_update = None
            if mood_id is None:
                create_or_update = db.create_mood
            else:
                create_or_update = db.update_mood
            mood_id = create_or_update(self.name, self.creator_id, self.params)
        return Mood(self.name, self.creator_id, deserialized, mood_id)


class GetMoodFromDBStrategy(GenerationStrategy):
    def generate(self):
        mood_id, params = None, None
        with DB() as db:
            mood_id, params = db.get_mood_by_name(self.name, self.creator_id)
        if mood_id is None:
            return None
        return Mood(self.name, self.creator_id, params, mood_id)


class DeleteMoodFromDBStrategy(GenerationStrategy):
    def generate(self):
        mood_id, params = None, None
        with DB() as db:
            mood_id, params = db.delete_mood(self.name, self.creator_id)
        if mood_id is None:
            return None
        return Mood(self.name, self.creator_id, params, mood_id)

class GetMoodFromDBWithIDStrategy(GenerationStrategy):
    def generate(self):
        mood_name, creator_id, params = None, None, None
        with DB() as db:
            mood_name, creator_id, params = db.get_mood_by_id(self.mood_id)
        if mood_name is None:
            return None
        return Mood(mood_name, creator_id, params, self.mood_id)

class GetRecentMoodsFromDBStrategy(GenerationStrategy):
    def generate(self):
        with DB() as db:
            recent_moods, other_users = db.get_recent_moods(self.creator_id)
            return [Mood(mood['mood_name'], other_user, mood['params'], mood['mood_id']) \
                for mood, other_user in zip(recent_moods, other_users)]
