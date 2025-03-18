import plugin

class RunAction(plugin.Action):
	def __init__(self):
		super().__init__("RunAction")

	def attach(self):
		super().attach()

class IdleAction(plugin.Action):
	def __init__(self):
		super().__init__("IdleAction")

class SimpleMovement(plugin.Plugin):
	def __init__(self):
		super().__init__("SimpleMovement")

		self.add_action(RunAction())
		self.add_action(IdleAction())
