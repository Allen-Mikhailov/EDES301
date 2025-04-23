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

    def pick_random_state():
        total_weight: number = 0

        for action_name: str in self.actions:
            action = self.actions[action_name]
            if action.is_ready:
                total_weight += action.random_weight

        alpha = random.random() * total_weight
        head = 0
        for action_name: str in self.actions:
            action = self.actions[action_name]

            if not action.is_ready:
                continue

            head += action.random_weight
            if head >= alpha:
                return action_name  

	def update_state(self):
        if current_action != None:
            return

		new_current_action: str | None = None
        alpha = random.random() * self.total_random_weight
        head = 0
        for action_name: str in self.actions:
            action = self.actions[action_name]
            head += action.random_weight
            if head >= alpha:
                new_current_action = action_name
                break
        
        if new_current_action != None:
            action = self.actions[new_current_action]

	def _release_action(self, action_name: str):
		self.actions[action_name].release()
		self.current_action = None
		self.update_state()

	def _attach_action(self, action_name):
		self.actions[action_name].attach()
		self.current_action = action_name

