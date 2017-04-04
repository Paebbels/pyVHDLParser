library IEEE;
use     IEEE.std_logic_1164.all;

entity entity1 is
	generic (
		WIDTH : natural := 0
	);
	port (
		Clock : bit;
		Reset : std_logic
	);
end entity;

library IEEE;
use     IEEE.numeric_std.all;

architecture arch1 of entity1 is
	constant const1 : std_logic := '1';
	function func1 return integer is
		constant const2 : positive := 2;
	begin
		-- this function is empty
	end function;
begin
	-- this architecture is empty
end architecture;

context ctx is
	library OSVVM;
	use     OSVVM.Scoreborad.all;
end context;


package pkg1 is
	constant const3 : natural;
	constant const4 : negative := 4;
end package;

package body pkg1 is
	constant const3 : natural := 3;

	function func2 return string is
	begin
		report Patrick severity failure;
	end function func0;

	procedure proc1 is
		variable var1 : string := "1";
		variable \var2\ : char := '2';
	begin
		-- this procedure is empty
	end procedure proc1;
end package body;
