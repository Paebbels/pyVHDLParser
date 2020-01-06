entity myEntity is
	generic (
		constant BITS : in positive := 8    -- 1 Byte
	);
	port (
		signal Clock : in  std_logic;  -- $IsClock:
		signal Reset : out std_logic := '0'
-- @Clock: generated reset pulse
	);
end entity;
