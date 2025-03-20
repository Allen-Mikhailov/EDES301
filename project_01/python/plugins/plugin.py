"""
--------------------------------------------------------------------------
Service
--------------------------------------------------------------------------
License:   
Copyright 2025 Allen Mikhailov

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Description

Requirements:
-

Uses:
-

"""
from __future__ import annotations
from state_machine import StateMachine

class Commander():
	drivers: dict[str, None] = {}
	plugins: dict[str, Plugin] = {}
	actions: dict[str, Action] = {}
	state_machine: StateMachine = StateMachine()

class Action:
	name: str = ""
	is_active: bool = False
	is_ready: bool = False
	force_priority: float = 0
	random_weight: float = 0
	commander: Commander | None = None

	parent_plugin: Plugin | None = None

	def __init__(self, name, force_priority=0, random_weight=0):
		self.name = name
		self.force_priority = force_priority
		self.random_weight = random_weight
	
	def attach_commander(self, machine):
		self.commander = machine

	def attach(self):
		self.is_active = True

	def release(self):
		self.is_active = False

	def loop(self):
		pass

class Plugin:
	name: str = ""
	actions: list[Action] = []
	commander: Commander | None = None

	def __init__(self, name: str):
		self.name = name

	def add_action(self, action: Action):
		action.parent_plugin = self
		self.actions.append(action)

	def attach_commander(self, machine):
		self.commander = machine
		for action in self.actions:
			action.attach_commander(machine)
        