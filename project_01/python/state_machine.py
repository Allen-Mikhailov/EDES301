# this only really exists as a seperate file to avoid circular dependencies 

class StateNode():
	name: str = ""
	is_active: bool = False
	is_ready: bool = False
	force_priority: float = 0
	random_weight: float = 0
	def __init__():
		pass
	
	

class StateMachine():
	actions: dict[str, StateNode] = {}
	current_action: str | None = None
	total_random_weight = 0
	def __init__(self) -> None:
		pass

	def add_action(self, action: StateNode):
		self.actions[action.name] = action
		self.total_random_weight += action.random_weight

	def set_ready_state(self, action_name: str, is_ready: bool):
		self.actions[action_name].is_ready = is_ready
		self.update_state()


	def update_state(self):
		new_current_action: StateNode | None = None


	def _release_action(self, action_name: str):
		self.actions[action_name].release()
		self.current_action = None
		self.update_state()

	def _attach_action(self, action_name):
		self.actions[action_name].attach()
		self.current_action = action_name

