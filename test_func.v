module test_func(x, c);

input [2:0] x;
output c;

assign c = (x[0] | x[1]) & x[2];

endmodule
