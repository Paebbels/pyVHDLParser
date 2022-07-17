-- Copryright 2016
library IEEE;
use     IEEE.std_logic_1164.all;

entity myEntity is
	generic (
		BITS : positive := 8
	);
	port (
		Clock   : in  std_logic;
		Output	: out	std_logic_vector(BITS - 1 downto 0)
	);
end entity;

use     IEEE.numeric_std.all;

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

use     std.textio.line;

package body Components is
	function func0(a : integer) return string is
		procedure proc0 is
		begin
		end procedure;
	begin
	end function;
end package body;

configuration config of myEntity is
	for rtl

	end for;
end configuration;
