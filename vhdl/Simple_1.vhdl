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
	process(Clock)
	begin
	end process;
	
end architecture;
