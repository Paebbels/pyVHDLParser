package body pkg0 is
	function func0 return integer is
		constant const3 : integer := 15;

		procedure proc1 is
			variable var5 : integer := 20;
		begin
		end procedure proc1;
	begin
		report Patrick severity failure;
	end function func0;
end package body;