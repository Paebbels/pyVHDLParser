entity myEntity0 is
	port(PORT0:positive);
end entity;

entity myEntity1 is
	port(PORT1 : in positive);
end entity;

entity myEntity2 is
	port ( PORT2 :in positive ) ;
end entity;

entity myEntity3 is
port (
PORT3 : in positive := 8
);
end entity;

entity myEntity4 is
	port (
		PORT4 : out boolean := true
	);
end entity;

entity myEntity5 is
	port (
		PORT5
		:
		inout
		boolean
		:=
		true
	);
end entity;

entity myEntity6 is
	port ( 
PORT6 
: 
buffer 
boolean 
:= 
true 
	)	;
end entity;

entity myEntity7 is
	port (
		PORT7a : in positive;
		PORT7b :out positive;
		PORT7c :inout positive
	);
end entity;

entity myEntity8 is
	port (
		PORT8a : positive := 8;
		PORT8b : positive := 8;
		PORT8c : positive := 8
	);
end entity;
