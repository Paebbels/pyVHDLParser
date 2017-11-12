entity system is
	procedure bar(constant x : in integer;variable y : out integer) is
	begin
		case x is
			when 2 =>
				return 5 + 2;
			when 2 * 5 =>
				--return b ; -- 10 + 5 * 2;
			when others =>
				--return c;
		end case;
	end procedure;

	function foo return integer is
	begin
		for i in 0 to 15 loop
			if (a <= b) or True then
				exit;
			elsif (c xor d) then
				exit bar ;
			elsif (e = f) then
				exit bar ;
			else
				next foo/*~*/;
			end if;
		end loop;
	end function;
end entity;


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
		/*procedure proc1 is
			variable var5 : integer := 20;
			variable \var6\ : string := "20";
		begin
		end procedure proc1;*/
	begin
		report Patrick severity failure;
	end function func0;
end package body;
