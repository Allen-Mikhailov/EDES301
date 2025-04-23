import plugin
from drivers.L293DNE import L293DNE

class RunAction(plugin.Action):
    hbrige: L293DNE
    def __init__(self, comm: plugin.Commander, hbrige: L293DNE):
		super().__init__("RunAction")

	def attach(self):
		super().attach()

class IdleAction(plugin.Action):
    hbrige: L293DNE
	def __init__(self, comm: plugin.Commander, hbrige: L293DNE):
		super().__init__("IdleAction")

class SimpleMovement(plugin.Plugin):
    hbrige: L293DNE
    def __init__(self, comm: plugin.Commander, hbrige: L293DNE):
		super().__init__("SimpleMovement")

        self.hbrige = hbrige

		self.add_action(RunAction(hbrige))
		self.add_action(IdleAction(hbrige))
