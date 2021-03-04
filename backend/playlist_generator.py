from .utils.db import DB

# TODO: complete stub code
class PlaylistGenerator:
    def __init__(self, mood_id, creator_id, params, strategy):
    	pass

    def set_strategy(self, strategy):
        self.strategy = strategy

    def generate(self):
    	return self.strategy(self.mood_id, self.creator_id, self.params).generate()

class GenerationStrategy:
    def __init__(self, mood_id, creator_id, params):
    		self.mood_id = mood_id
        self.creator_id = creator_id
        self.params = params
    
    def generate(self):
        raise NotImplementedError

class GetPlaylistsFromDBStrategy(GenerationStrategy):
	def generate(self):
		return None
