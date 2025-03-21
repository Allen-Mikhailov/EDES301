# this only really exists as a seperate file to avoid circular dependencies 

import plugins.plugin as plugins

class StateMachine():
	actions: dict[str, plugins.Action] = {}
	current_action: str | None = None
	total_random_weight = 0
	def __init__(self) -> None:
		pass

	def add_action(self, action: plugins.Action):
		self.actions[action.name] = action
		self.total_random_weight += action.random_weight

	def update_state(self):
		new_current_action = None


	def release_action(self, action_name: str):
		self.actions[action_name].release()
		self.current_action = None
		self.update_state()

	def _attach_action(self, action_name):
		self.actions[action_name].attach()
		self.current_action = action_name

