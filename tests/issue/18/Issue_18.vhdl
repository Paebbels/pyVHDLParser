library ieee;
use ieee.std_logic_1164.all;


entity transfer is
  generic (
    num_bits1 : positive := 2;
    num_bits2 : positive := 4
  );
  port (
    clk_src1   : in  std_logic;
    reset_src1 : in  std_logic;
    clk_src2   : in  std_logic;
    reset_src2 : in  std_logic;
    clk_dest   : in  std_logic;
    reset_dest : in  std_logic;
    flags_src1 : in  std_logic_vector(num_bits1-1 downto 0);
    flags_src2 : in  std_logic_vector(num_bits2-1 downto 0);
    flags_out  : out std_logic_vector(num_bits1+num_bits2-1 downto 0)
  );
end entity;

architecture rtl of transfer is

  signal reg_catch1   : std_logic_vector(flags_src1'range);
  signal reg_catch2   : std_logic_vector(flags_src2'range);
  signal reg_dest_r   : std_logic_vector(num_bits1+num_bits2-1 downto 0);
  signal conf_src1_r1 : std_logic_vector(flags_src1'range);
  signal conf_src1_r2 : std_logic_vector(flags_src1'range);
  signal conf_src2_r1 : std_logic_vector(flags_src2'range);
  signal conf_src2_r2 : std_logic_vector(flags_src2'range);
  signal conf_dest    : std_logic_vector(num_bits1+num_bits2-1 downto 0);

  -- Could be placed in a constraints file
  attribute ASYNC_REG : string;
  attribute ASYNC_REG of conf_src1_r1 : signal is "TRUE";
  attribute ASYNC_REG of conf_src1_r2 : signal is "TRUE";
  attribute ASYNC_REG of conf_src2_r1 : signal is "TRUE";
  attribute ASYNC_REG of conf_src2_r2 : signal is "TRUE";
  attribute ASYNC_REG of reg_dest_r   : signal is "TRUE";
  attribute ASYNC_REG of flags_out    : signal is "TRUE";

begin

  -- Retain the flag until it has been read in the slower clock domain.
  process(clk_src1)
  begin
    if rising_edge(clk_src1) then
      if reset_src1 = '1' then
        conf_src1_r1 <= (others => '0');
        conf_src1_r2 <= (others => '0');
        reg_catch1   <= (others => '0');
      else
        conf_src1_r1 <= flags_out(num_bits1-1+num_bits2 downto num_bits2);
        conf_src1_r2 <= conf_src1_r1;
        -- Remember the flags until they are acknowledged
        for i in flags_src1'range loop
          if conf_src1_r2(i) = '1' then
            reg_catch1(i) <= '0';
          elsif flags_src1(i) = '1' then
            reg_catch1(i) <= '1';
          end if;
        end loop;
      end if;
    end if;
  end process;

  -- Retain the flag until it has been read in the slower clock domain.
  process(clk_src2)
  begin
    if rising_edge(clk_src2) then
      if reset_src2 = '1' then
        conf_src2_r1 <= (others => '0');
        conf_src2_r2 <= (others => '0');
        reg_catch2   <= (others => '0');
      else
        conf_src2_r1 <= flags_out(num_bits2-1 downto 0);
        conf_src2_r2 <= conf_src2_r1;
        -- Remember the flags until they are acknowledged
        for i in flags_src2'range loop
          if conf_src2_r2(i) = '1' then
            reg_catch2(i) <= '0';
          elsif flags_src2(i) = '1' then
            reg_catch2(i) <= '1';
          end if;
        end loop;
      end if;
    end if;
  end process;

  process(clk_dest)
  begin
    if rising_edge(clk_dest) then
      if reset_dest = '1' then
        reg_dest_r <= (others => '0');
        flags_out  <= (others => '0');
      else
        reg_dest_r <= reg_catch1 & reg_catch2;
        flags_out  <= reg_dest_r;
      end if;
    end if;
  end process;

end architecture;
