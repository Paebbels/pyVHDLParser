package body pkg0 is
	function func0 return integer is
	begin
	end function;
	
	function func1(param10 : integer; param11 : integer) return integer is
	begin
	end function;
	
	function func2(param20:integer;param21:integer)return integer is
	begin
	end function;
	
	function
	func3
	(
	param30
	:
	integer
	)
	return
	integer
	is
	begin
	end function;
	
	function func4 parameter(param40 : integer) return integer is
	begin
	end function;
	
	function func5 generic(GEN0 : positive := 8) parameter (param40 : integer) return integer is
	begin
	end function;
	
	function func6
		generic (
			GEN60 : positive := 8;
			GEN61 : positive := 8
		)
		parameter (
			param40 : integer;
			param41 : positive := 6
		)
	return integer is
	begin
	end function;
	
	pure function func7(param70 : integer; param71 : integer) return integer is
	begin
	end function;
	
	impure function func7(param70 : integer; param71 : integer) return integer is
	begin
	end function;
end package body;