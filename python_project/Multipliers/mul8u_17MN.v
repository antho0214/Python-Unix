module mul8u_17MN (A, B, O);

input [7:0] A;
input [7:0] B;
output [15:0] O;

wire sig_71,sig_79,sig_293,sig_338,sig_340,sig_345;

assign sig_71 = B[6] & A[7];
assign sig_79 = B[7] & A[7];
assign sig_293 = A[6] | A[7];
assign sig_338 = sig_293 & B[7];
assign sig_340 = A[6] & B[5];
assign sig_345 = sig_79 ^ sig_338;

assign O[15] = sig_79;
assign O[14] = sig_345;
assign O[13] = sig_340;
assign O[12] = sig_71;
assign O[11] = sig_71;
assign O[10] = 1'b0;
assign O[9] = 1'b0;
assign O[8] = sig_71;
assign O[7] = sig_79;
assign O[6] = 1'b0;
assign O[5] = 1'b0;
assign O[4] = 1'b0;
assign O[3] = 1'b0;
assign O[2] = sig_71;
assign O[1] = 1'b0;
assign O[0] = 1'b0;

endmodule


