# this only really exists as a seperate file to avoid circular dependencies 

import plugins.plugin as plugins

class StateMachine():
	actions: dict[str, plugins.Action] = {}
	current_action: str | None = None
	def __init__(self) -> None:
		pass

	def update_state(self):
		


	def release_action(self, action_name: str):
		action = self.actions[action_name].release()

	def attach_action(self, action_name)