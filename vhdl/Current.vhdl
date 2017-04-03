entity system is
	generic (
		WIDTH : natural := 0
	);
	port (
		Clock : bit;
		Reset : std_logic
	);
end entity;


-- This is the first package
-- described in two comment lines
architecture rtl of system is
begin
	process (Clock, Reset)
		variable halt : bit;
	begin
	end process;
end architecture;

context ctx is
	library OSVVM;
	use     OSVVM.Scoreborad.all;
end context;

library IEEE;
use     IEEE.std_logic_vector.all;

package pkg0 is
	function func0 return integer;
end package;

package body pkg0 is
	constant const3 : std_logic := '0';
	function func1 return integer is
		constant const3 : std_logic := '0';
		procedure proc1 is
			variable var5 : integer := 20;
			variable \var6\ : string := "20";
		begin
		end procedure proc1;
	begin
		report Patrick severity failure;
	end function func0;
end package body;


