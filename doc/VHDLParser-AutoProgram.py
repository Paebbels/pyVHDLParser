# EMACS settings: -*-  tab-width: 2; indent-tabs-mode: t; python-indent-offset: 2 -*-
# vim: tabstop=2:shiftwidth=2:noexpandtab
# kate: tab-width 2; replace-tabs off; indent-width 2;
# ==============================================================================
# Authors:              Patrick Lehmann
#
# Python Main Module:   Entry point for Sphinx analysis tools (e.g. autoprogram).
#
# Description:
# ------------------------------------
# Undocumented
#
# License:
# ==============================================================================
# Copyright 2017-2020 Patrick Lehmann - Boetzingen, Germany
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
#
from sys import path as sys_path

sys_path.append("..")

from pyVHDLParser.CLI.VHDLParser import Application

# entry point
parser = Application(sphinx=True).MainParser
