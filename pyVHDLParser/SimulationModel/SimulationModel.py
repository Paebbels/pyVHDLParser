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
# Copyright 2017-2023 Patrick Lehmann - Boetzingen, Germany                                                            #
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
from pyTooling.Decorators                     import export

from pyVHDLParser.SimulationModel.EventSystem import ProjectedWaveform, Waveform, Scheduler, Event


@export
class Simulation:
	def __init__(self):
		self._signals =     []
		self._processes =   []
		self._scheduler =   Scheduler()

	def AddSignal(self, signal):
		self._signals.append(signal)
		signal.Simulator = self

	def AddProcess(self, process):
		self._processes.append(process)

	def Initialize(self):
		for signal in self._signals:
			signal.Initialize()
		for process in self._processes:
			process.Initialize()

	def Run(self):
		iterators = [(p,iter(p._generator())) for p in self._processes]

		for process,iterator in iterators:
			signalChanges,time = next(iterator)
			for signal,value in signalChanges:
				signal.SetValue(value)

			self._scheduler.AddEvent(Event(self._scheduler._now + time, process))


			print(time)



		for signal in self._signals:
			print("{signal!s}: {wave}".format(signal=signal, wave=signal._waveform._transactions))

	@property
	def Now(self):
		return self._scheduler._now


	def ExportVCD(self, filename):
		pass


@export
class Path:
	def __init__(self, name, path):
		self._name =    name
		self._path =    path

	def __repr__(self):
		return self._path

	def __str__(self):
		return self._name


@export
class Signal:
	def __init__(self, path, subType, initializer=None):
		self._path =              path
		self._subType =           subType
		self._initializer =       initializer
		self._drivingValue =      None
		self._projectedWaveform = ProjectedWaveform(self)
		self._waveform =          Waveform(self)
		self.Simulator =          None

	def Initialize(self):
		if (self._initializer is not None):
			result = self._initializer()
		else:
			result = self._subType.Attributes.Low()
		self._waveform.Initialize(result)

	def SetValue(self, value):
		self._waveform.AddEvent(self.Simulator.Now, value)

	def __repr__(self):
		return "{path!r}: {value}".format(path=self._path, value="------")

	def __str__(self):
		return "{path!s}: {value}".format(path=self._path, value="------")


@export
class Process:
	def __init__(self, path, generator, sensitivityList=None):
		self._path =            path
		self._sensitivityList = sensitivityList
		self._generator =       generator
		self._constants =       []
		self._variables =       []
		self._outputs =         []
		self._instructions =    []

	def Initialize(self):
		pass


@export
class Source:
	pass


@export
class Driver(Source):
	pass


@export
class ResolutionFunction:
	def __init__(self):
		self._function =  None


@export
class DrivingValue:
	pass
