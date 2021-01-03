# ==============================================================================
# Authors:            Patrick Lehmann
#
# Python frontend:    A streaming VHDL parser
#
# License:
# ==============================================================================
# Copyright 2017-2021 Patrick Lehmann - Boetzingen, Germany
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
from argparse       import RawDescriptionHelpFormatter
from platform       import system as platform_system
from textwrap       import dedent, wrap

from pyExceptions                     import ExceptionBase
from pyAttributes.ArgParseAttributes  import ArgParseMixin, DefaultAttribute, CommandAttribute, ArgumentAttribute, CommonSwitchArgumentAttribute
from pyMetaClasses                    import Singleton
from pyTerminalUI                     import LineTerminal, Severity

from pyVHDLParser.Blocks              import MetaBlock

from pyVHDLParser.CLI.Token           import TokenStreamHandlers
from pyVHDLParser.CLI.Block           import BlockStreamHandlers
from pyVHDLParser.CLI.Group           import GroupStreamHandlers
from pyVHDLParser.CLI.CodeDOM         import CodeDOMHandlers


__author__ =      "Patrick Lehmann"
__copyright__ =   "Copyright 2017-2021 Patrick Lehmann - Boetzingen, Germany\n" + \
                  "Copyright 2016-2017 Patrick Lehmann - Dresden, Germany"
__maintainer__ =  "Patrick Lehmann"
__email__ =       "Patrick.Lehmann@plc2.de"
__version__ =     "0.6.0"
__status__ =      "Alpha"
__license__ =     "Apache License 2.0"
__api__ = [
	'printImportError',
	'Application'
]
__all__ = __api__


def printImportError(ex):
	platform = platform_system()
	print("IMPORT ERROR: One or more Python packages are not available in your environment.")
	print("Missing package: '{0}'\n".format(ex.name))
	if (platform == "Windows"):
		print("Run: 'py.exe -3 -m pip install -r requirements.txt'\n")
	elif (platform == "Linux"):
		print("Run: 'python3 -m pip install -r requirements.txt'\n")
	exit(1)


class Application(LineTerminal, ArgParseMixin, TokenStreamHandlers, BlockStreamHandlers, GroupStreamHandlers, CodeDOMHandlers):
	HeadLine =    "pyVHDLParser - Test Application"

	# load platform information (Windows, Linux, Darwin, ...)
	__PLATFORM =  platform_system()

	def __init__(self, debug=False, verbose=False, quiet=False, sphinx=False):
		super().__init__(verbose, debug, quiet)

		# Initialize the Terminal class
		# --------------------------------------------------------------------------
		Singleton.Register(LineTerminal, self)

		# Late-initialize Block classes
		# --------------------------------------------------------------------------
		for block in MetaBlock.BLOCKS:
			try:
				block.__cls_init__()
			except AttributeError:
				pass

		# Call the constructor of the ArgParseMixin
		# --------------------------------------------------------------------------
		textWidth = min(self.Width, 160)
		description = dedent("""\
			Test application to test pyVHDLParser capabilities.
			""")
		epilog = "\n".join(wrap(dedent("""\
		  pyVHDLParser is a streaming parser to read and understand VHDL code equipped with comments for documentation extraction.
		  """), textWidth, replace_whitespace=False))

		class HelpFormatter(RawDescriptionHelpFormatter):
			def __init__(self, *args, **kwargs):
				kwargs['max_help_position'] = 30
				kwargs['width'] =             textWidth
				super().__init__(*args, **kwargs)

		ArgParseMixin.__init__(
			self,
	    description=description,
			epilog=epilog,
	    formatter_class=HelpFormatter,
	    add_help=False
	  )

		# If executed in Sphinx to auto-document CLI arguments, exit now
		# --------------------------------------------------------------------------
		if sphinx:
			return

		# Change error and warning reporting
		# --------------------------------------------------------------------------
		self._LOG_MESSAGE_FORMAT__[Severity.Fatal]   = "{DARK_RED}[FATAL] {message}{NOCOLOR}"
		self._LOG_MESSAGE_FORMAT__[Severity.Error]   = "{RED}[ERROR] {message}{NOCOLOR}"
		self._LOG_MESSAGE_FORMAT__[Severity.Warning] = "{YELLOW}[WARNING] {message}{NOCOLOR}"
		self._LOG_MESSAGE_FORMAT__[Severity.Normal]  = "{GRAY}{message}{NOCOLOR}"

	# class properties
	# ============================================================================
	@property
	def Platform(self):
		return self.__PLATFORM

	def PrintHeadline(self):
		self.WriteNormal(dedent("""\
			{HEADLINE}{line}
			{headline: ^80s}
			{line}""").format(line="=" * 80, headline=self.HeadLine, **LineTerminal.Foreground))

	# ============================================================================
	# Common commands
	# ============================================================================
	# common arguments valid for all commands
	# ----------------------------------------------------------------------------
	@CommonSwitchArgumentAttribute("-d", "--debug",   dest="debug",   help="Enable debug mode.")
	@CommonSwitchArgumentAttribute("-v", "--verbose", dest="verbose", help="Print out detailed messages.")
	@CommonSwitchArgumentAttribute("-q", "--quiet",   dest="quiet",   help="Reduce messages to a minimum.")
	def Run(self):
		ArgParseMixin.Run(self)

	@DefaultAttribute()
	def HandleDefault(self, _):
		self.PrintHeadline()
		self.MainParser.print_help()

		self.WriteNormal("")
		self.exit()

	# ----------------------------------------------------------------------------
	# create the sub-parser for the "help" command
	# ----------------------------------------------------------------------------
	@CommandAttribute("help", help="Display help page(s) for the given command name.")
	@ArgumentAttribute(metavar="Command", dest="Command", type=str, nargs="?", help="Print help page(s) for a command.")
	def HandleHelp(self, args):
		self.PrintHeadline()

		if (args.Command is None):
			self.MainParser.print_help()
		elif (args.Command == "help"):
			self.WriteError("This is a recursion ...")
		else:
			try:
				self.SubParsers[args.Command].print_help()
			except KeyError:
				self.WriteError("Command {0} is unknown.".format(args.Command))

		self.WriteNormal("")
		self.exit()

	# ----------------------------------------------------------------------------
	# create the sub-parser for the "version" command
	# ----------------------------------------------------------------------------
	@CommandAttribute("version", help="Display tool and version information.")
	def HandleInfo(self, args):
		self.PrintHeadline()

		copyrights = __copyright__.split("\n", 1)
		self.WriteNormal("Copyright:  {0}".format(copyrights[0]))
		for copyright in copyrights[1:]:
			self.WriteNormal("            {0}".format(copyright))
		self.WriteNormal("License:    {0}".format(__license__))
		authors = __author__.split(", ")
		self.WriteNormal("Authors:    {0}".format(authors[0]))
		for author in authors[1:]:
			self.WriteNormal("            {0}".format(author))
		self.WriteNormal("Version:    {0}".format(__version__))
		self.exit()


# main program
def main(): # mccabe:disable=MC0001
	"""This is the entry point for pyVHDLParser written as a function.

	1. It extracts common flags from the script's arguments list, before :py:class:`~argparse.ArgumentParser` is fully loaded.
	2. It creates an instance of VHDLParser and hands over to a class based execution.
	   All is wrapped in a big ``try..except`` block to catch every unhandled exception.
	3. Shutdown the script and return its exit code.
	"""
	from sys import argv as sys_argv

	debug =   "-d"        in sys_argv
	verbose = "-v"        in sys_argv
	quiet =   "-q"        in sys_argv

	try:
		# handover to a class instance
		app = Application(debug, verbose, quiet)
		app.Run()
		app.exit()

	# except (CommonException, ConfigurationException) as ex:
	# 	print("{RED}ERROR:{NOCOLOR} {message}".format(message=ex.message, **Init.Foreground))
	# 	cause = ex.__cause__
	# 	if isinstance(cause, FileNotFoundError):
	# 		print("{YELLOW}  FileNotFound:{NOCOLOR} '{cause}'".format(cause=str(cause), **Init.Foreground))
	# 	elif isinstance(cause, NotADirectoryError):
	# 		print("{YELLOW}  NotADirectory:{NOCOLOR} '{cause}'".format(cause=str(cause), **Init.Foreground))
	# 	elif isinstance(cause, ParserException):
	# 		print("{YELLOW}  ParserException:{NOCOLOR} {cause}".format(cause=str(cause), **Init.Foreground))
	# 		cause = cause.__cause__
	# 		if (cause is not None):
	# 			print("{YELLOW}    {name}:{NOCOLOR} {cause}".format(name=cause.__class__.__name__, cause= str(cause), **Init.Foreground))
	#
	# 	if (not (verbose or debug)):
	# 		print()
	# 		print("{CYAN}  Use '-v' for verbose or '-d' for debug to print out extended messages.{NOCOLOR}".format(**Init.Foreground))
	# 	LineTerminal.exit(1)

	except ExceptionBase as ex:                 LineTerminal.printExceptionBase(ex)
	except NotImplementedError as ex:           LineTerminal.printNotImplementedError(ex)
	#except ImportError as ex:                   printImportError(ex)
	except Exception as ex:                     LineTerminal.printException(ex)


# entry point
if __name__ == "__main__":
	LineTerminal.versionCheck((3,8,0))
	main()
