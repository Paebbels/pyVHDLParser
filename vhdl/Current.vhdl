library IEEE, PoC;
use     IEEE.std_logic_1164.all, PoC.ocram.all;

context OSVVM is
	use OSVVM.Scoreboard.all;
end context;

entity myEntity is
	port (
		foo : in string := "my name";
		bar : out negative
	);
end entity;

/*
package pkg0 is
	generic (
		foo : string;
		bar : negative
	);

	use PoC.ocram.all;
	constant const0 : integer := 5;
	constant const1 : integer;
	--function func0 return integer;
end package;

package body pkg0 is
	--function func0(a : integer; b : integer) return integer is
	constant const1 : integer := 10;
	/*function func0 return integer is
		constant const3 : integer := 15;

		/*function func1 return integer is
			constant const4 : integer := 20;
		begin
		end function func0;*//*
	begin
	end function func0;
	*//*
end package body;
*/