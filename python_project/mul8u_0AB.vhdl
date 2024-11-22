entity full_adder is
port (A,B,Ci : in std_logic;
S,Co : out std_logic);
end full_adder;
architecture full_adder_struct of full_adder is
signal w1,w2,w3,w4: std_logic;
begin
w1 <= A xor B;
S <= w1 xor Ci;
w2 <= A and B;
w3 <= A and Ci;
w4 <= Ci and B;
Co <= w2 or w3 or w4;
end full_adder_struct;
