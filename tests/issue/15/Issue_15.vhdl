library ieee;
use ieee.std_logic_1164.all;


entity retime is
  generic (
    num_bits : positive := 2
  );
  port (
    clk_src    : in  std_logic;
    reset_src  : in  std_logic;
    clk_dest   : in  std_logic;
    reset_dest : in  std_logic;
    flags_in   : in  std_logic_vector(num_bits-1 downto 0);
    flags_out  : out std_logic_vector(num_bits-1 downto 0)
  );
end entity;

architecture rtl of retime is

  signal reg_capture : std_logic_vector(num_bits-1 downto 0);
  signal reg_retime  : std_logic_vector(num_bits-1 downto 0);

  -- Could be placed in a constraints file
  attribute ASYNC_REG : string;
  attribute ASYNC_REG of reg_retime : signal is "TRUE";
  attribute ASYNC_REG of flags_out  : signal is "TRUE";

begin

  -- Remove glitches from any unregistered combinatorial logic on the source data.
  -- Glitches must not be captured by accident in the new clock domain.
  process(clk_src)
  begin
    if rising_edge(clk_src) then
      if reset_src = '1' then
        reg_capture <= (others => '0');
      else
        reg_capture <= flags_in;
      end if;
    end if;
  end process;

  process(clk_dest)
  begin
    if rising_edge(clk_dest) then
      if reset_dest = '1' then
        reg_retime <= (others => '0');
        flags_out  <= (others => '0');
      else
        reg_retime <= reg_capture;
        flags_out  <= reg_retime;
      end if;
    end if;
  end process;

end architecture;
