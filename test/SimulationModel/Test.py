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
# load dependencies
from pyVHDLParser.SimulationModel.SimulationModel import Simulation, Path, Signal, Process
from pyVHDLParser.TypeSystem.std_logic_1164       import Std_Logic


sim = Simulation()

sig1 = Signal(Path("signal1", "/signal1"), Std_Logic)
sig2 = Signal(Path("signal2", "/signal2"), Std_Logic)

sim.AddSignal(sig1)
sim.AddSignal(sig2)

def p1():
	zero = Std_Logic.Attributes.Value("0")
	one =  Std_Logic.Attributes.Value("1")
	for i in range(10):
		yield ([
				(sig1, zero)
		  ], 10)
		yield ([
			  (sig1, one)
		  ], 10)

def p2():
	zero = Std_Logic.Attributes.Value("0")
	one =  Std_Logic.Attributes.Value("1")
	for i in range(20):
		yield ([
				(sig2, one)
		  ], 5)
		yield ([
			  (sig2, zero)
		  ], 5)

proc1 = Process(Path("proc1", "/proc1"), p1)
proc2 = Process(Path("proc2", "/proc2"), p2)

sim.AddProcess(proc1)
sim.AddProcess(proc2)

sim.Initialize()
sim.Run()
sim.ExportVCD("wave.vcd")
