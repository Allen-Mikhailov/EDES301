import plugin
from drivers.L293DNE import L293DNE

class RunAction(plugin.Action):
    hbrige: L293DNE
    def __init__(self, comm: plugin.Commander, hbrige: L293DNE):
		super().__init__(comm, "RunAction", random_weight=1)
        self.hbrige = hbrige

	def attach(self):
		super().attach()
        self.hbrige.move_m1(1)
        self.hbrige.move_m2(-1)

    def loop(self):
        super().loop()
        self.hbrige.move_m1(0)
        self.hbrige.move_m2(0)


    def release(self):
        super().release()
        hbrige.

class IdleAction(plugin.Action):
    hbrige: L293DNE
	def __init__(self, comm: plugin.Commander, hbrige: L293DNE):
		super().__init__(comm, "IdleAction")

class SimpleMovement(plugin.Plugin):
    hbrige: L293DNE
    def __init__(self, comm: plugin.Commander, hbrige: L293DNE):
		super().__init__(comm, "SimpleMovement")

        self.hbrige = hbrige

		self.add_action(RunAction(comm, hbrige))
		self.add_action(IdleAction(comm, hbrige))
