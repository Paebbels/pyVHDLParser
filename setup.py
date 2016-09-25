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
# Copyright 2007-2016 Patrick Lehmann - Dresden, Germany
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
from setuptools import setup

dataFiles = []

setup(
	name="pyVHDLParser",
	version="0.1.0",
	author="Patrick Lehmann",
	author_email="Patrick.Lehmann@tu-dresden.de",
	description="A streaming-based VHDL parser.",
	long_description=open("README.rst").read(),
	url="https://github.com/Paebbels/pyVHDLParser",
	packages=[
		"pyVHDLParser",
		"pyVHDLParser.Block",
		"pyVHDLParser.Block.Assignments",
		"pyVHDLParser.Block.Attribute",
		"pyVHDLParser.Block.ControlStructure",
		"pyVHDLParser.Block.Generate",
		"pyVHDLParser.Block.Instantiation",
		"pyVHDLParser.Block.List",
		"pyVHDLParser.Block.ObjectDeclaration",
		"pyVHDLParser.Block.Reference",
		"pyVHDLParser.Block.Reporting",
		"pyVHDLParser.Block.Sequential",
		"pyVHDLParser.Block.Structural",
		"pyVHDLParser.Block.Type",
		"pyVHDLParser.Filter",
		"pyVHDLParser.Graph",
		"pyVHDLParser.Group",
		"pyVHDLParser.Model",
		"pyVHDLParser.StyleCheck",
		"pyVHDLParser.Token"
	],
	package_data={
		'pyVHDLParser': dataFiles
	},
	zip_safe=False,
	classifiers=[
		"Development Status :: 3 - Alpha",
		"License :: OSI Approved :: Apache License 2.0",
		"Natural Language :: English",
		"Intended Audience :: Developers",
		"Programming Language :: Python :: 3.5",
		"Operating System :: Microsoft :: Windows",
		"Operating System :: MacOS :: MacOS X",
		"Operating System :: POSIX :: Linux"
	]
)  # nopep8
