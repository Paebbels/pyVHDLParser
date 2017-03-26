architecture arch of ent is
begin
	process
	begin
	end process;

	process is
	begin
	end process;

	process(all)
	begin
	end process;

	process(all)is
	begin
	end process;

	process (all) is
	begin
	end process;

	process (clock,reset) is
	begin
	end process;

	process ( clock , reset , all) is
	begin
	end process;

	process
		constant const0 : integer := 5;
	begin
	end process;

	process is
		constant const0 : integer := 10;
	begin
	end process;

	process(all)
		constant const0 : integer := 15;
	begin
	end process;
end architecture;
