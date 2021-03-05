from .utils.db import DB

class Playlist:
	def __init__(self, creator_id, mood_id, idx, uri):
		self.creator_id = creator_id
		self.mood_id = mood_id
		self.idx = idx
		self.uri = uri
	
	def to_dict(self):
		return {'mood_id': self.mood_id, 'idx': self.idx, 'uri': self.uri}

# TODO: complete stub code
class PlaylistGenerator:
	def __init__(self, mood_id, creator_id, uri, strategy):
		self.mood_id = mood_id
		self.creator_id = creator_id
		self.uri = uri
		self.strategy = strategy

	def set_strategy(self, strategy):
		self.strategy = strategy

	def generate(self):
		return self.strategy(self.mood_id, self.creator_id, self.uri).generate()

class GenerationStrategy:
	def __init__(self, mood_id, creator_id, uri):
		self.mood_id = mood_id
		self.creator_id = creator_id
		self.uri = uri

	def generate(self):
		raise NotImplementedError

class GetPlaylistsFromDBStrategy(GenerationStrategy):
	def generate(self):
		rows = None
		with DB() as db:
			rows = db.get_mood_playlists(self.creator_id, self.mood_id)
		if rows is None:
			return None
		return [Playlist(row[0], row[1], row[2], row[3]) for row in rows]

class StorePlaylistInDBStrategy(GenerationStrategy):
	def generate(self):
		idx = None
		with DB() as db:
			idx = db.create_playlist_on_mood(self.creator_id, self.mood_id, self.uri)
		if idx is None:
			return None
		return Playlist(self.creator_id, self.mood_id, idx, self.uri)