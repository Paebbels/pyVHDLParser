entity myEntity0 is
	generic(GEN0:positive);
end entity;

entity myEntity1 is
	generic(GEN1 : positive);
end entity;

entity myEntity2 is
	generic ( GEN2 : positive ) ;
end entity;

entity myEntity3 is
generic (
GEN3 : positive := 8
);
end entity;

entity myEntity4 is
	generic (
		GEN4 : boolean := true
	);
end entity;

entity myEntity5 is
	generic (
		GEN5
		:
		boolean
		:=
		true
	);
end entity;

entity myEntity6 is
	generic ( 
GEN6 
: 
boolean 
:= 
true 
	)	;
end entity;

entity myEntity7 is
	generic (
		GEN7a : positive;
		GEN7b : positive;
		GEN7c : positive
	);
end entity;

entity myEntity8 is
	generic (
		GEN8a : positive := 8;
		GEN8b : positive := 8;
		GEN8c : positive := 8
	);
end entity;
