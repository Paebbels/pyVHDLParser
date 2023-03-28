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
import functools
import time
from typing import Dict


class ExecutionTimer:
	_times: Dict = None

	def __init__(self):
		self._times = {}

	def AddExecutionTime(self, function, executionTime):
		try:
			self._times[function].append(executionTime)
		except ValueError:
			self._times[function] = [ executionTime ]


class ExecutionCounter:
	_counts: Dict = None

	def __init__(self):
		self._counts = {}

	def IncrementCallCounter(self, function):
		try:
			self._counts[function] += 1
		except ValueError:
			self._counts[function] = 1


def LogExecutionTime(function):
	"""Measure the runtime execution time of functions and methods."""

	@functools.wraps(function)
	def wrapper(*args, **kwargs):
		start_time = time.perf_counter()
		value = function(*args, **kwargs)
		end_time = time.perf_counter()

		__TIMER__.AddExecutionTime(function, end_time - start_time)

		return value

	return wrapper

def LogExecutionCount(function):
	"""Count how often a functions or methods was called."""

	@functools.wraps(function)
	def wrapper(*args, **kwargs):
		value = function(*args, **kwargs)

		__COUNTER__.IncrementCallCounter(function)

		return value

	return wrapper

__TIMER__ =   ExecutionTimer()
__COUNTER__ = ExecutionCounter()

# def debug(func):
# 	"""Print the function signature and return value"""
# 	@functools.wraps(func)
# 	def wrapper_debug(*args, **kwargs):
# 		args_repr = [repr(a) for a in args]                      # 1
# 		kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
# 		signature = ", ".join(args_repr + kwargs_repr)           # 3
# 		print(f"Calling {func.__name__}({signature})")
# 		value = func(*args, **kwargs)
# 		print(f"{func.__name__!r} returned {value!r}")           # 4
# 		return value
# 	return wrapper_debug

# class CountCalls:
# 	def __init__(self, func):
# 		functools.update_wrapper(self, func)
# 		self.func = func
# 		self.num_calls = 0
#
# 	def __call__(self, *args, **kwargs):
# 		self.num_calls += 1
# 		print(f"Call {self.num_calls} of {self.func.__name__!r}")
# 		return self.func(*args, **kwargs)
#
# def set_unit(unit):
#     """Register a unit on a function"""
#     def decorator_set_unit(func):
#         func.unit = unit
#         return func
#     return decorator_set_unit
