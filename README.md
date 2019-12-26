![PyPI - License](https://img.shields.io/pypi/l/pyVHDLParser)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/Paebbels/pyVHDLParser) 
![GitHub release (latest by date)](https://img.shields.io/github/v/release/Paebbels/pyVHDLParser)
[![Documentation Status](https://readthedocs.org/projects/pyvhdlparser/badge/?version=latest)](https://pyVHDLParser.readthedocs.io/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/pyVHDLParser)](https://pypi.org/project/pyVHDLParser/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyVHDLParser)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/pyVHDLParser)
![PyPI - Status](https://img.shields.io/pypi/status/pyVHDLParser)

<!--
   [![Build Status](https://travis-ci.org/Paebbels/pyVHDLParser.svg?branch=master)](https://travis-ci.org/Paebbels/pyVHDLParser)
-->

# pyVHDLParser

This is a token-stream based parser for VHDL-2008.

Main goals:
 * slice an input document into text blocks which are categorized
 * group text blocks for fast-forward scanning
 * provide a generic VHDL language model

Use cases:
 * generate documentation by using the fast-forward scanner
 * generate a document/language model by using the grouped text-block scanner
 * extract compile orders and other dependency graphs
 * generate highlighted syntax
 * re-annotate documenting comments to their objects for doc extraction

Long time goals:
 * A Sphinx language plugin for VHDL 

## Basic Concept

[![][concept]][concept]

[concept]: https://raw.githubusercontent.com/Paebbels/pyVHDLParser/master/docs/images/Linking_TokenBlockGroup.png

## Example 1

This is an input file:

```VHDL
-- Copryright 2016
library IEEE;
use     IEEE.std_logic_1164.all;

entity myEntity is
  generic (
    BITS : positive := 8
  );
  port (
    Clock   : in   std_logic;
    Output  : out  std_logic_vector(BITS - 1 downto 0)
  );
end entity;

architecture rtl of myEntity is
  constant const0 : integer := 5;
begin
  process(Clock)
  begin
  end process;
end architecture;

library IEEE, PoC;
use     PoC.Utils.all, PoC.Common.all;

package pkg0 is
  function func0(a : integer) return string;
end package;

package body Components is
  function func0(a : integer) return string is
    procedure proc0 is
    begin
    end procedure;
  begin
  end function
end package body;
```

### Step 1
The input file (stream of characters) is translated into stream of basic tokens:
* `StartOfDocumentToken`
* `LinebreakToken`
* `SpaceToken`
  * `IndentationToken`
* `StringToken`
* `CharacterToken`
  * `FusedCharacterToken`
* CommentToken
  * `SingleLineCommentToken`
  * `MultiLineCommentToken`
* `EndOfDocumentToken`


The stream looks like this:
```
<StartOfDocumentToken>
<SLCommentToken '-- Copryright 2016\n'  ................ at 1:1>
<StringToken    'library'  ............................. at 2:1>
<SpaceToken     ' '  ................................... at 2:8>
<StringToken    'IEEE'  ................................ at 2:9>
<CharacterToken ';'  ................................... at 2:13>
<LinebreakToken ---------------------------------------- at 2:14>
<StringToken    'use'  ................................. at 3:1>
<SpaceToken     '     '  ............................... at 3:4>
<StringToken    'IEEE'  ................................ at 3:9>
<CharacterToken '.'  ................................... at 3:13>
<StringToken    'std_logic_1164'  ...................... at 3:14>
<CharacterToken '.'  ................................... at 3:28>
<StringToken    'all'  ................................. at 3:29>
<CharacterToken ';'  ................................... at 3:32>
<LinebreakToken ---------------------------------------- at 3:33>
<LinebreakToken ---------------------------------------- at 4:1>
<StringToken    'entity'  .............................. at 5:1>
<SpaceToken     ' '  ................................... at 5:7>
<StringToken    'myEntity'  ............................ at 5:8>
<SpaceToken     ' '  ................................... at 5:16>
<StringToken    'is'  .................................. at 5:17>
<LinebreakToken ---------------------------------------- at 5:19>
<IndentToken    '\t'  .................................. at 6:1>
<StringToken    'generic'  ............................. at 6:2>
<SpaceToken     ' '  ................................... at 6:9>
<CharacterToken '('  ................................... at 6:10>
<LinebreakToken ---------------------------------------- at 6:11>
<IndentToken    '\t\t'  ................................ at 7:1>
<StringToken    'BITS'  ................................ at 7:3>
<SpaceToken     ' '  ................................... at 7:7>
<CharacterToken ':'  ................................... at 7:8>
<SpaceToken     ' '  ................................... at 7:8>
<StringToken    'positive'  ............................ at 7:10>
<SpaceToken     ' '  ................................... at 7:18>
<FusedCharToken ':='  .................................. at 7:19>
<SpaceToken     ' '  ................................... at 7:21>
<StringToken    '8'  ................................... at 7:22>
<LinebreakToken ---------------------------------------- at 7:23>
<IndentToken    '\t'  .................................. at 8:1>
<CharacterToken ')'  ................................... at 8:2>
<CharacterToken ';'  ................................... at 8:3>
<LinebreakToken ---------------------------------------- at 8:4>
<IndentToken    '\t'  .................................. at 9:1>
<StringToken    'port'  ................................ at 9:2>
<SpaceToken     ' '  ................................... at 9:6>
<CharacterToken '('  ................................... at 9:7>
<LinebreakToken ---------------------------------------- at 9:8>
<IndentToken    '\t\t'  ................................ at 10:1>
<StringToken    'Clock'  ............................... at 10:3>
<SpaceToken     '   '  ................................. at 10:8>
<CharacterToken ':'  ................................... at 10:11>
<SpaceToken     ' '  ................................... at 10:11>
<StringToken    'in'  .................................. at 10:13>
<SpaceToken     '  '  .................................. at 10:15>
<StringToken    'std_logic'  ........................... at 10:17>
<CharacterToken ';'  ................................... at 10:26>
<LinebreakToken ---------------------------------------- at 10:27>
<IndentToken    '\t\t'  ................................ at 11:1>
<StringToken    'Output'  .............................. at 11:3>
<SpaceToken     '       '  ................................... at 11:9>
<CharacterToken ':'  ................................... at 11:10>
<SpaceToken     ' '  ................................... at 11:10>
<StringToken    'out'  ................................. at 11:12>
<SpaceToken     '       '  ................................... at 11:15>
<StringToken    'std_logic_vector'  .................... at 11:16>
<CharacterToken '('  ................................... at 11:32>
<StringToken    'BITS'  ................................ at 11:33>
<SpaceToken     ' '  ................................... at 11:37>
<CharacterToken '-'  ................................... at 11:38>
<SpaceToken     ' '  ................................... at 11:38>
<StringToken    '1'  ................................... at 11:40>
<SpaceToken     ' '  ................................... at 11:41>
<StringToken    'downto'  .............................. at 11:42>
<SpaceToken     ' '  ................................... at 11:48>
<StringToken    '0'  ................................... at 11:49>
<CharacterToken ')'  ................................... at 11:50>
<LinebreakToken ---------------------------------------- at 11:51>
<IndentToken    '\t'  .................................. at 12:1>
<CharacterToken ')'  ................................... at 12:2>
<CharacterToken ';'  ................................... at 12:3>
<LinebreakToken ---------------------------------------- at 12:4>
<StringToken    'end'  ................................. at 13:1>
<SpaceToken     ' '  ................................... at 13:4>
<StringToken    'entity'  .............................. at 13:5>
<CharacterToken ';'  ................................... at 13:11>
<LinebreakToken ---------------------------------------- at 13:12>
<LinebreakToken ---------------------------------------- at 14:1>
<StringToken    'architecture'  ........................ at 15:1>
<SpaceToken     ' '  ................................... at 15:13>
<StringToken    'rtl'  ................................. at 15:14>
<SpaceToken     ' '  ................................... at 15:17>
<StringToken    'of'  .................................. at 15:18>
<SpaceToken     ' '  ................................... at 15:20>
<StringToken    'myEntity'  ............................ at 15:21>
<SpaceToken     ' '  ................................... at 15:29>
<StringToken    'is'  .................................. at 15:30>
<LinebreakToken ---------------------------------------- at 15:32>
<IndentToken    '\t'  .................................. at 16:1>
<StringToken    'constant'  ............................ at 16:2>
<SpaceToken     ' '  ................................... at 16:10>
<StringToken    'const0'  .............................. at 16:11>
<SpaceToken     ' '  ................................... at 16:17>
<CharacterToken ':'  ................................... at 16:18>
<SpaceToken     ' '  ................................... at 16:18>
<StringToken    'integer'  ............................. at 16:20>
<SpaceToken     ' '  ................................... at 16:27>
<FusedCharToken ':='  .................................. at 16:28>
<SpaceToken     ' '  ................................... at 16:30>
<StringToken    '5'  ................................... at 16:31>
<CharacterToken ';'  ................................... at 16:32>
<LinebreakToken ---------------------------------------- at 16:33>
<StringToken    'begin'  ............................... at 17:1>
<LinebreakToken ---------------------------------------- at 17:6>
<IndentToken    '\t'  .................................. at 18:1>
<StringToken    'process'  ............................. at 18:2>
<CharacterToken '('  ................................... at 18:9>
<StringToken    'Clock'  ............................... at 18:10>
<CharacterToken ')'  ................................... at 18:15>
<LinebreakToken ---------------------------------------- at 18:16>
<IndentToken    '\t'  .................................. at 19:1>
<StringToken    'begin'  ............................... at 19:2>
<LinebreakToken ---------------------------------------- at 19:7>
<IndentToken    '\t'  .................................. at 20:1>
<StringToken    'end'  ................................. at 20:2>
<SpaceToken     ' '  ................................... at 20:5>
<StringToken    'process'  ............................. at 20:6>
<CharacterToken ';'  ................................... at 20:13>
<LinebreakToken ---------------------------------------- at 20:14>
<StringToken    'end'  ................................. at 21:1>
<SpaceToken     ' '  ................................... at 21:4>
<StringToken    'architecture'  ........................ at 21:5>
<CharacterToken ';'  ................................... at 21:17>
<LinebreakToken ---------------------------------------- at 21:18>
<LinebreakToken ---------------------------------------- at 22:1>
<StringToken    'library'  ............................. at 23:1>
<SpaceToken     ' '  ................................... at 23:8>
<StringToken    'IEEE'  ................................ at 23:9>
<CharacterToken ','  ................................... at 23:13>
<SpaceToken     ' '  ................................... at 23:14>
<StringToken    'PoC'  ................................. at 23:15>
<CharacterToken ';'  ................................... at 23:18>
<LinebreakToken ---------------------------------------- at 23:19>
<StringToken    'use'  ................................. at 24:1>
<SpaceToken     '     '  ............................... at 24:4>
<StringToken    'PoC'  ................................. at 24:9>
<CharacterToken '.'  ................................... at 24:12>
<StringToken    'Utils'  ............................... at 24:13>
<CharacterToken '.'  ................................... at 24:18>
<StringToken    'all'  ................................. at 24:19>
<CharacterToken ','  ................................... at 24:22>
<SpaceToken     ' '  ................................... at 24:23>
<StringToken    'PoC'  ................................. at 24:24>
<CharacterToken '.'  ................................... at 24:27>
<StringToken    'Common'  .............................. at 24:28>
<CharacterToken '.'  ................................... at 24:34>
<StringToken    'all'  ................................. at 24:35>
<CharacterToken ';'  ................................... at 24:38>
<LinebreakToken ---------------------------------------- at 24:39>
<LinebreakToken ---------------------------------------- at 25:1>
<StringToken    'package'  ............................. at 26:1>
<SpaceToken     ' '  ................................... at 26:8>
<StringToken    'pkg0'  ................................ at 26:9>
<SpaceToken     ' '  ................................... at 26:13>
<StringToken    'is'  .................................. at 26:14>
<LinebreakToken ---------------------------------------- at 26:16>
<IndentToken    '\t'  .................................. at 27:1>
<StringToken    'function'  ............................ at 27:2>
<SpaceToken     ' '  ................................... at 27:10>
<StringToken    'func0'  ............................... at 27:11>
<CharacterToken '('  ................................... at 27:16>
<StringToken    'a'  ................................... at 27:17>
<SpaceToken     ' '  ................................... at 27:18>
<CharacterToken ':'  ................................... at 27:19>
<SpaceToken     ' '  ................................... at 27:19>
<StringToken    'integer'  ............................. at 27:21>
<CharacterToken ')'  ................................... at 27:28>
<SpaceToken     ' '  ................................... at 27:29>
<StringToken    'return'  .............................. at 27:30>
<SpaceToken     ' '  ................................... at 27:36>
<StringToken    'string'  .............................. at 27:37>
<CharacterToken ';'  ................................... at 27:43>
<LinebreakToken ---------------------------------------- at 27:44>
<StringToken    'end'  ................................. at 28:1>
<SpaceToken     ' '  ................................... at 28:4>
<StringToken    'package'  ............................. at 28:5>
<CharacterToken ';'  ................................... at 28:12>
<LinebreakToken ---------------------------------------- at 28:13>
<LinebreakToken ---------------------------------------- at 29:1>
<StringToken    'package'  ............................. at 30:1>
<SpaceToken     ' '  ................................... at 30:8>
<StringToken    'body'  ................................ at 30:9>
<SpaceToken     ' '  ................................... at 30:13>
<StringToken    'Components'  .......................... at 30:14>
<SpaceToken     ' '  ................................... at 30:24>
<StringToken    'is'  .................................. at 30:25>
<LinebreakToken ---------------------------------------- at 30:27>
<IndentToken    '\t'  .................................. at 31:1>
<StringToken    'function'  ............................ at 31:2>
<SpaceToken     ' '  ................................... at 31:10>
<StringToken    'func0'  ............................... at 31:11>
<CharacterToken '('  ................................... at 31:16>
<StringToken    'a'  ................................... at 31:17>
<SpaceToken     ' '  ................................... at 31:18>
<CharacterToken ':'  ................................... at 31:19>
<SpaceToken     ' '  ................................... at 31:19>
<StringToken    'integer'  ............................. at 31:21>
<CharacterToken ')'  ................................... at 31:28>
<SpaceToken     ' '  ................................... at 31:29>
<StringToken    'return'  .............................. at 31:30>
<SpaceToken     ' '  ................................... at 31:36>
<StringToken    'string'  .............................. at 31:37>
<SpaceToken     ' '  ................................... at 31:43>
<StringToken    'is'  .................................. at 31:44>
<LinebreakToken ---------------------------------------- at 31:46>
<IndentToken    '\t\t'  ................................ at 32:1>
<StringToken    'procedure'  ........................... at 32:3>
<SpaceToken     ' '  ................................... at 32:12>
<StringToken    'proc0'  ............................... at 32:13>
<SpaceToken     ' '  ................................... at 32:18>
<StringToken    'is'  .................................. at 32:19>
<LinebreakToken ---------------------------------------- at 32:21>
<IndentToken    '\t\t'  ................................ at 33:1>
<StringToken    'begin'  ............................... at 33:3>
<LinebreakToken ---------------------------------------- at 33:8>
<IndentToken    '\t\t'  ................................ at 34:1>
<StringToken    'end'  ................................. at 34:3>
<SpaceToken     ' '  ................................... at 34:6>
<StringToken    'procedure'  ........................... at 34:7>
<CharacterToken ';'  ................................... at 34:16>
<LinebreakToken ---------------------------------------- at 34:17>
<IndentToken    '\t'  .................................. at 35:1>
<StringToken    'begin'  ............................... at 35:2>
<LinebreakToken ---------------------------------------- at 35:7>
<IndentToken    '\t'  .................................. at 36:1>
<StringToken    'end'  ................................. at 36:2>
<SpaceToken     ' '  ................................... at 36:5>
<StringToken    'function'  ............................ at 36:6>
<LinebreakToken ---------------------------------------- at 36:14>
<StringToken    'end'  ................................. at 37:1>
<SpaceToken     ' '  ................................... at 37:4>
<StringToken    'package'  ............................. at 37:5>
<SpaceToken     ' '  ................................... at 37:12>
<StringToken    'body'  ................................ at 37:13>
<CharacterToken ';'  ................................... at 37:17>
<LinebreakToken ---------------------------------------- at 37:18>
```

[![Screenshot][10]][10]

### Step 2
The token stream from step 1 is translated into typed tokens like
`DelimiterToken` (:), `EndToken` (;) or subtypes of `KeywordToken`.
These tokens are then grouped into blocks.

The example generates:
```
[StartOfDocumentBlock]
[Blocks.CommentBlock            '-- Copryright 2016\n'                                         at (line:   1, col:  1) .. (line:   1, col: 19)]
[Library.LibraryBlock           'library '                                                     at (line:   2, col:  1) .. (line:   2, col:  8)]
[Library.LibraryNameBlock       'IEEE'                                                         at (line:   2, col:  9) .. (line:   2, col: 13)]
[Library.LibraryEndBlock        ';'                                                            at (line:   2, col: 13) .. (line:   2, col: 13)]
[LinebreakBlock                                                                                at (line:   2, col: 14) .. (line:   2, col: 14)]
[Use.UseBlock                   'use     '                                                     at (line:   3, col:  1) .. (line:   3, col:  8)]
[Use.UseNameBlock               'IEEE.std_logic_1164.all'                                      at (line:   3, col:  9) .. (line:   3, col: 32)]
[Use.UseEndBlock                ';'                                                            at (line:   3, col: 32) .. (line:   3, col: 32)]
[LinebreakBlock                                                                                at (line:   3, col: 33) .. (line:   3, col: 33)]
[EmptyLineBlock                                                                                at (line:   4, col:  1) .. (line:   4, col:  1)]
[Entity.NameBlock               'entity myEntity is'                                           at (line:   5, col:  1) .. (line:   5, col: 19)]
[LinebreakBlock                                                                                at (line:   5, col: 19) .. (line:   5, col: 19)]
[IndentationBlock                length=1 (2)                                                  at (line:   6, col:  1) .. (line:   6, col:  1)]
[GenericList.OpenBlock          'generic ('                                                    at (line:   6, col:  2) .. (line:   6, col: 10)]
[LinebreakBlock                                                                                at (line:   6, col: 11) .. (line:   6, col: 11)]
[IndentationBlock                length=2 (4)                                                  at (line:   7, col:  1) .. (line:   7, col:  2)]
[GenericList.ItemBlock          'BITS : positive := 8\n\t'                                     at (line:   7, col:  3) .. (line:   8, col:  1)]
[GenericList.CloseBlock         ');'                                                           at (line:   8, col:  2) .. (line:   8, col:  3)]
[LinebreakBlock                                                                                at (line:   8, col:  4) .. (line:   8, col:  4)]
[IndentationBlock                length=1 (2)                                                  at (line:   9, col:  1) .. (line:   9, col:  1)]
[PortList.OpenBlock             'port ('                                                       at (line:   9, col:  2) .. (line:   9, col:  7)]
[LinebreakBlock                                                                                at (line:   9, col:  8) .. (line:   9, col:  8)]
[IndentationBlock                length=2 (4)                                                  at (line:  10, col:  1) .. (line:  10, col:  2)]
[PortList.ItemBlock             'Clock   : in  std_logic'                                      at (line:  10, col:  3) .. (line:  10, col: 26)]
[PortList.DelimiterBlock        ';'                                                            at (line:  10, col: 26) .. (line:  10, col: 26)]
[LinebreakBlock                                                                                at (line:  10, col: 27) .. (line:  10, col: 27)]
[IndentationBlock                length=2 (4)                                                  at (line:  11, col:  1) .. (line:  11, col:  2)]
[PortList.ItemBlock             'Output\t: out\tstd_logic_vector(BITS - 1 downto 0)\n\t'       at (line:  11, col:  3) .. (line:  12, col:  1)]
[PortList.CloseBlock            ');'                                                           at (line:  12, col:  2) .. (line:  12, col:  3)]
[LinebreakBlock                                                                                at (line:  12, col:  4) .. (line:  12, col:  4)]
[Entity.EndBlock                'end entity;'                                                  at (line:  13, col:  1) .. (line:  13, col: 11)]
[LinebreakBlock                                                                                at (line:  13, col: 12) .. (line:  13, col: 12)]
[EmptyLineBlock                                                                                at (line:  14, col:  1) .. (line:  14, col:  1)]
[Architecture.NameBlock         'architecture rtl of myEntity is'                              at (line:  15, col:  1) .. (line:  15, col: 32)]
[LinebreakBlock                                                                                at (line:  15, col: 32) .. (line:  15, col: 32)]
[IndentationBlock                length=1 (2)                                                  at (line:  16, col:  1) .. (line:  16, col:  1)]
[Constant.ConstantBlock         'constant const0 : integer := 5;'                              at (line:  16, col:  2) .. (line:  16, col: 32)]
[LinebreakBlock                                                                                at (line:  16, col: 33) .. (line:  16, col: 33)]
[EmptyLineBlock                                                                                at (line:  17, col:  6) .. (line:  17, col:  6)]
[IndentationBlock                length=1 (2)                                                  at (line:  18, col:  1) .. (line:  18, col:  1)]
[Process.OpenBlock              'process('                                                     at (line:  18, col:  2) .. (line:  18, col:  9)]
[SensitivityList.ItemBlock      'Clock'                                                        at (line:  18, col: 10) .. (line:  18, col: 15)]
[Process.OpenBlock2*            ')'                                                            at (line:  18, col: 15) .. (line:  18, col: 15)]
[LinebreakBlock                                                                                at (line:  18, col: 16) .. (line:  18, col: 16)]
...
```

The following screenshot shows the resulting stream of blocks:
[![][20]][20]


[outdated]
The block stream can also be "opened" to show the stream of tokens within each block. This is shown in the next screenshot:
[![][21]][21]

### Step 3
The stream of blocks from step 2 is transformed into a stream of groups.

### Step 4
One of many post processing steps could be to remove whitespaces, indentation and comment blocks. So a filter can be applied to remove these block types. Additionally, multiparted blocks (e.g. if a comment or linebreak was inserted between consecutive code sequences, which belong to one block) can be fused to one single block.

This screenshot shows the filtered results:
[![][30]][30] 

 [10]: https://raw.githubusercontent.com/Paebbels/pyVHDLParser/master/docs/screens/TokenStream_Example_1.png
 [20]: https://raw.githubusercontent.com/Paebbels/pyVHDLParser/master/docs/screens/BlockStream_Example_1.png
 [21]: https://raw.githubusercontent.com/Paebbels/pyVHDLParser/master/docs/screens/BlockStream_Uses_Detailed.png
 [30]: https://raw.githubusercontent.com/Paebbels/pyVHDLParser/master/docs/screens/BlockStream_Uses_Fused.png

## Example 2 - Simple_1

This is an input file:

```VHDL
-- Copryright 2016
library IEEE;
use     IEEE.std_logic_1164.all;
use      IEEE.numeric_std.all;

entity myEntity is
  generic (
    BITS : positive := 8
  );
  port (
    Clock   : in  std_logic;
    Reset   : in  std_logic;
    Output  : out  std_logic_vector(BITS - 1 downto 0)
  );
end entity;

architecture rtl of myEntity is

begin

end architecture;
```

This is the result stream:
[![][40]][40] 

And this is the filtered and fused result stream:
[![][41]][41]

 [40]: https://raw.githubusercontent.com/Paebbels/pyVHDLParser/master/docs/screens/BlockStream_Simple_1.png
 [41]: https://raw.githubusercontent.com/Paebbels/pyVHDLParser/master/docs/screens/BlockStream_Simple_1_Fused.png


#### License

Licensed under [Apache License 2.0](LICENSE.md).
