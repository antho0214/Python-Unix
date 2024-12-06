Library IEEE;
use IEEE.std_logic_1164.all;
use std.textio.all;
entity mul8u_17MN is
port (A : in std_logic_vector(7 downto 0);
B : in std_logic_vector(7 downto 0);
O : out std_logic_vector(15 downto 0)
);
end mul8u_17MN;
architecture mul8u_17MN_struct of mul8u_17MN is
signal sig_71,sig_79,sig_293,sig_338,sig_340,sig_345: std_logic;
begin
sig_71 <= B(6) and A(7);
sig_79 <= B(7) and A(7);
sig_293 <= A(6) or A(7);
sig_338 <= sig_293 and B(7);
sig_340 <= A(6) and B(5);
sig_345 <= sig_79 xor sig_338;
O(15) <= sig_79;
O(14) <= sig_345;
O(13) <= sig_340;
O(12) <= sig_71;
O(11) <= sig_71;
O(10) <= '0';
O(9) <= '0';
O(8) <= sig_71;
O(7) <= sig_79;
O(6) <= '0';
O(5) <= '0';
O(4) <= '0';
O(3) <= '0';
O(2) <= sig_71;
O(1) <= '0';
O(0) <= '0';
end mul8u_17MN_struct;
