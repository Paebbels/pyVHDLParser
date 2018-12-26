# EMACS settings: -*-	tab-width: 2; indent-tabs-mode: t; python-indent-offset: 2 -*-
# vim: tabstop=2:shiftwidth=2:noexpandtab
# kate: tab-width 2; replace-tabs off; indent-width 2;
# ==============================================================================
# Authors:            Patrick Lehmann
#
# Python functions:   A streaming VHDL parser
#
# Description:
# ------------------------------------
#		TODO:
#
# License:
# ==============================================================================
# Copyright 2017-2019 Patrick Lehmann - Boetzingen, Germany
# Copyright 2016-2017 Patrick Lehmann - Dresden, Germany
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
#
class Scheduler:
	def __init__(self):
		self._now =             0
		self._globalTimeLine =  TimeLine()
	
	def AddEvent(self, relTime):
		pass

	def GetNextTime(self):
		return None


class Event:
	def __init__(self, time, process):
		self._previous =  None
		self._next =      None
		self._time =      time
		self.WakeList =   [process]
	
	def AddProcess(self, process):
		self.WakeList.append(process)
	

class Transaction:
	def __init__(self, time, value):
		self._time =  time
		self._value = value
	
	def __str__(self):
		return "({time}, {value})".format(time=self._time, value=self._value)
	
	__repr__ = __str__
		

class TimeLine:
	def __init__(self):
		self._transactions =    []
	
	def AddTransaction(self, transaction):
		pass


class Waveform:
	def __init__(self, signal):
		self._signal =          signal
		self._transactions =    []
	
	def Initialize(self, value):
		self._transactions.append(Transaction(0, value))
	
	def AddEvent(self, time, value):
		self._transactions.append(Transaction(time, value))
	

class ProjectedWaveform(TimeLine):
	def __init__(self, signal):
		self._signal =          signal
