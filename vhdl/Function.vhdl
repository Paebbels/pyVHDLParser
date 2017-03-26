package pkg0 is
	function func0 return integer;
	function func1(param0:integer)return integer;
	function func2 ( param0 : integer ) return integer;
	function func3(param0 : integer; param1 : integer) return integer;
end package;

package body pkg0 is
	function func0 return integer is
	begin
	end function;

	function func0 return integer is begin end;
	function func0 return integer is begin end ;
	function func0 return integer is begin end function;

	function func1(param0:integer)return integer is
	begin
	end function;

	function func1(param0:integer)return integer is	begin
	end function;

	function func2 ( param0 : integer ) return integer is
	begin
	end function;

	function func2 ( param0 : integer ) return integer is begin
	end function;

	function func3(param0 : integer; param1 : integer) return integer is
	begin
	end function func0;
end package body;