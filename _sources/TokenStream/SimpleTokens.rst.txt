.. _tokstm-simpletoken:

Simple Tokens
#############

Simple tokens, are tokens created by the :ref:`tokstm-tokenizer`.

The tokenizer has no deep knowledge of the VHDL language, thus it can only detect
a limited number of distinct tokens. These token require only a context of up to
two characters while parsing.

**List of simple tokens:**

+--------------------------+-------------------------+-------------------------------------------------------+
| Kind                     | Examples                | pyVHDLParser Token Class                              |
+==========================+=========================+=======================================================+
| Single character         | ``;``, ``(``            | :class:`~pyVHDLParser.Token.CharacterToken`           |
+--------------------------+-------------------------+-------------------------------------------------------+
| Multiple characters      | ``<=``, ``:=``, ``**``  | :class:`~pyVHDLParser.Token.FusedCharacterToken`      |
+--------------------------+-------------------------+-------------------------------------------------------+
| Whitespace (space, tab)  |                         | :class:`~pyVHDLParser.Token.SpaceToken`               |
+--------------------------+-------------------------+-------------------------------------------------------+
| Word                     | ``entity``, ``xor``     | :class:`~pyVHDLParser.Token.WordToken`                |
+--------------------------+-------------------------+-------------------------------------------------------+
| Single-line comment      | ``-- TODO``             | :class:`~pyVHDLParser.Token.SingleLineCommentToken`   |
+--------------------------+-------------------------+-------------------------------------------------------+
| Multi-line comment       | ``/*comment*/``         | :class:`~pyVHDLParser.Token.MultiLineCommentToken`    |
+--------------------------+-------------------------+-------------------------------------------------------+
| Integer literal          | ``42``                  | :class:`~pyVHDLParser.Token.IntegerLiteralToken`      |
+--------------------------+-------------------------+-------------------------------------------------------+
| Real literal             | ``1.25``                | :class:`~pyVHDLParser.Token.RealLiteralToken`         |
+--------------------------+-------------------------+-------------------------------------------------------+
| Character literal        | ``'a'``, ``'Z'``        | :class:`~pyVHDLParser.Token.CharacterLiteralToken`    |
+--------------------------+-------------------------+-------------------------------------------------------+
| String literal           | ``"hello"``             | :class:`~pyVHDLParser.Token.StringLiteralToken`       |
+--------------------------+-------------------------+-------------------------------------------------------+
| Bit string literal       | ``x"42"``               | :class:`~pyVHDLParser.Token.BitStringLiteralToken`    |
+--------------------------+-------------------------+-------------------------------------------------------+
| Extended identifiers     | ``\$cell35\``           | :class:`~pyVHDLParser.Token.ExtendedIdentifierToken`  |
+--------------------------+-------------------------+-------------------------------------------------------+
| Tool directives          |                         | :class:`~pyVHDLParser.Token.DirectiveToken`           |
+--------------------------+-------------------------+-------------------------------------------------------+
| Linebreak                | ``\n``                  | :class:`~pyVHDLParser.Token.LineBreakToken`           |
+--------------------------+-------------------------+-------------------------------------------------------+
| indentation              | ``\t``                  | :class:`~pyVHDLParser.Token.IndentationToken`         |
+--------------------------+-------------------------+-------------------------------------------------------+
