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

use     STD.TextIO.all;

architecture rtl of myEntity is

begin
	process(Clock)
	begin
	end process;
	
end architecture;

library PoC;
use     PoC.Utils.all;
use     PoC.Common.all;
use     PoC.Strings.all;

package Components is

end package;


library PoC;
use     PoC.Vectors.all;

package body Components is

end package body;
