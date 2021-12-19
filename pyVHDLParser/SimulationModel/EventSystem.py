# ==================================================================================================================== #
#            __     ___   _ ____  _     ____                                                                           #
#  _ __  _   \ \   / / | | |  _ \| |   |  _ \ __ _ _ __ ___  ___ _ __                                                  #
# | '_ \| | | \ \ / /| |_| | | | | |   | |_) / _` | '__/ __|/ _ \ '__|                                                 #
# | |_) | |_| |\ V / |  _  | |_| | |___|  __/ (_| | |  \__ \  __/ |                                                    #
# | .__/ \__, | \_/  |_| |_|____/|_____|_|   \__,_|_|  |___/\___|_|                                                    #
# |_|    |___/                                                                                                         #
# ==================================================================================================================== #
# Authors:                                                                                                             #
#   Patrick Lehmann                                                                                                    #
#                                                                                                                      #
# License:                                                                                                             #
# ==================================================================================================================== #
# Copyright 2017-2021 Patrick Lehmann - Boetzingen, Germany                                                            #
# Copyright 2016-2017 Patrick Lehmann - Dresden, Germany                                                               #
#                                                                                                                      #
# Licensed under the Apache License, Version 2.0 (the "License");                                                      #
# you may not use this file except in compliance with the License.                                                     #
# You may obtain a copy of the License at                                                                              #
#                                                                                                                      #
#   http://www.apache.org/licenses/LICENSE-2.0                                                                         #
#                                                                                                                      #
# Unless required by applicable law or agreed to in writing, software                                                  #
# distributed under the License is distributed on an "AS IS" BASIS,                                                    #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.                                             #
# See the License for the specific language governing permissions and                                                  #
# limitations under the License.                                                                                       #
# ==================================================================================================================== #
#
from pyTooling.Decorators             import export


@export
class Scheduler:
	def __init__(self):
		self._now =             0
		self._globalTimeLine =  TimeLine()

	def AddEvent(self, relTime):
		pass

	def GetNextTime(self):
		return None


@export
class Event:
	def __init__(self, time, process):
		self._previous =  None
		self._next =      None
		self._time =      time
		self.WakeList =   [process]

	def AddProcess(self, process):
		self.WakeList.append(process)


@export
class Transaction:
	def __init__(self, time, value):
		self._time =  time
		self._value = value

	def __str__(self):
		return "({time}, {value})".format(time=self._time, value=self._value)

	__repr__ = __str__


@export
class TimeLine:
	def __init__(self):
		self._transactions =    []

	def AddTransaction(self, transaction):
		pass


@export
class Waveform:
	def __init__(self, signal):
		self._signal =          signal
		self._transactions =    []

	def Initialize(self, value):
		self._transactions.append(Transaction(0, value))

	def AddEvent(self, time, value):
		self._transactions.append(Transaction(time, value))


@export
class ProjectedWaveform(TimeLine):
	def __init__(self, signal):
		self._signal =          signal
