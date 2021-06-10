# =============================================================================
#            __     ___   _ ____  _     ____
#  _ __  _   \ \   / / | | |  _ \| |   |  _ \ __ _ _ __ ___  ___ _ __
# | '_ \| | | \ \ / /| |_| | | | | |   | |_) / _` | '__/ __|/ _ \ '__|
# | |_) | |_| |\ V / |  _  | |_| | |___|  __/ (_| | |  \__ \  __/ |
# | .__/ \__, | \_/  |_| |_|____/|_____|_|   \__,_|_|  |___/\___|_|
# |_|    |___/
# =============================================================================
# Authors:            Patrick Lehmann
#
# Package installer:  A streaming-based VHDL parser.
#
#
# License:
# ============================================================================
# Copyright 2017-2021 Patrick Lehmann - Bötzingen, Germany
# Copyright 2016-2017 Patrick Lehmann - Dresden, Germany
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#		http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# ============================================================================
#
from pathlib    import Path
from setuptools import setup as setuptools_setup, find_packages as setuptools_find_packages

gitHubNamespace = "Paebbels"
projectName =     "pyVHDLParser"

# Read README for upload to PyPI
readmeFile = Path("README.md")
with readmeFile.open("r") as file:
	long_description = file.read()

# Read requirements file and add them to package dependency list
requirementsFile = Path("requirements.txt")
with requirementsFile.open("r") as file:
	requirements = [line for line in file.readlines()]

# Derive URLs
sourceCodeURL =     "https://github.com/{namespace}/{projectName}".format(namespace=gitHubNamespace, projectName=projectName)
documentationURL =  "https://{namespace}.github.io/{projectName}/using/py/index.html".format(namespace=gitHubNamespace, projectName=projectName)

# Assemble all package information
setuptools_setup(
	name=projectName,
	version="0.6.3",

	author="Patrick Lehmann",
	author_email="Paebbels@gmail.com",
	# maintainer="Patrick Lehmann",
	# maintainer_email="Paebbels@gmail.com",

	description="A streaming-based VHDL parser.",
	long_description=long_description,
	long_description_content_type="text/markdown",

	url=sourceCodeURL,
	project_urls={
		'Documentation': documentationURL,
		'Source Code':   sourceCodeURL,
		'Issue Tracker': sourceCodeURL + "/issues"
	},
	# download_url="https://github.com/Paebbels/pyVHDLParser/tarball/0.1.0",

	packages=setuptools_find_packages(),
	entry_points={
		'console_scripts': [
			"VHDLParser = pyVHDLParser.CLI.VHDLParser:main"
		]
	},
	classifiers=[
		"License :: OSI Approved :: Apache Software License",
		"Operating System :: OS Independent",
		"Programming Language :: Python :: 3 :: Only",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
		"Development Status :: 2 - Pre-Alpha",
		#   "Development Status :: 3 - Alpha",
		#		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
		"Topic :: Software Development :: Code Generators",
		"Topic :: Software Development :: Compilers",
		"Topic :: Software Development :: Testing",
		"Topic :: Utilities"
	],
	keywords="Python3 Parser VHDL Streaming Documentation",

	python_requires='>=3.8',
	install_requires=requirements,
)
