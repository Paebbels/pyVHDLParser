# pyVHDLParser

[![Apache License 2.0](https://img.shields.io/github/license/VLSI-EDA/PoC.svg?style=flat)](LICENSE.md)

This is a token-stream based parser for VHDL-2008.

Main goals:
 * slice a input document into text blocks, which are categorized
 * group text blocks for fast-forward scanning
 * provide a generic VHDL language model

Use cases:
 * generate a documentations by using the fast-forward scanner
 * generate a document/language model by using the grouped text-block scanner
 * extract compile orders and other dependency graphs
 * generate highlighted syntax
 * re-annotate documenting comments to there objects for doc extraction

Long time goals:
 * A Sphinx language plugin for VHDL 


## Example 1 - Use clauses

This is a input file:

```VHDL
use lib0.pkg0.all;

use lib1.pkg1.all ;

use lib2.pkg2.all; -- comment

use		lib3.pkg3.all		;

use lib4.pkg4.const4;
```

### Step 1
The input file is translated into basic tokens: `SpaceToken`, `StringToken`, `CharacterToken`. The stream looks like this:

```
StartOfDocumentToken
StringToken("use")
SpaceToken(" ")
StringToken("lib0")
CharacterToken(".")
StringToken("pkg0")
CharacterToken(".")
StringToken("all")
CharacterToken(";")
CharacterToken("\n")
...
CharacterToken("\n")
EndOfDocumentToken
```

### Step 2
The tokens from step 1 are translated into special tokens like `DelimiterToken`, `IndentationToken`, and  subtypes of `KeywordToken`. These tokens are grouped into block. In the *Uses* example, the first 8 tokens form a `UseBlock`.

The following screenshot shows the resulting stream of blocks:
[![][1]][1]

The block stream can also be "opened" to show the stream of tokens within each block. This is shown in the next screenshot:
[![][2]][2]

### Step 3
One of many post processing steps could be to remove whitespaces, indentation and comment blocks. So a filter can be applied to remove these block types. Additionally, multiparted blocks (e.g. if a comment or linebreak was inserted between consecutive code sequences, which belong to one block) can be fused to one single block.

This screenshot shows the filtered results:
[![][3]][3] 

 [1]: https://raw.githubusercontent.com/Paebbels/pyVHDLParser/master/docs/screens/BlockStream_Uses.png
 [2]: https://raw.githubusercontent.com/Paebbels/pyVHDLParser/master/docs/screens/BlockStream_Uses_Detailed.png
 [3]: https://raw.githubusercontent.com/Paebbels/pyVHDLParser/master/docs/screens/BlockStream_Uses_Fused.png

## Example 2 - Simple_1

This is a input file:

```VHDL
-- Copryright 2016
library IEEE;
use     IEEE.std_logic_1164.all;
use			IEEE.numeric_std.all;

entity myEntity is
	generic (
		BITS : positive := 8
	);
	port (
		Clock   : in  std_logic;
		Reset   : in	std_logic;
		Output	: out	std_logic_vector(BITS - 1 downto 0)
	);
end entity;

architecture rtl of myEntity is

begin

end architecture;
```

And this is the filtered and fused result stream:
[![][4]][4] 

 [4]: https://raw.githubusercontent.com/Paebbels/pyVHDLParser/master/docs/screens/BlockStream_Simple_1_Fused.png


#### License

Licensed under [Apache License 2.0](LICENSE.md).
