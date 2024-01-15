module conv_addr
#(
	parameter ADDR_WIDTH = 18,
	parameter K_PARAMS   = 16
)(
  // ----------- CLOCK & RESET ----------
	input  logic clk,
  input  logic rst_n,
  // -------------- INPUTS --------------
	input  logic                i_enb_M0,
	input  logic                i_enb_CN,
	input  logic                i_enb_K,
	input  logic [K_PARAMS-1:0] i_w,
	// ------------- OUTPUTS --------------
	output logic [ADDR_WIDTH-1:0] o_addr,
	output logic                  o_end_kernel
);

logic [K_PARAMS-1:0] LKA, FKA;
logic [1:0]          odd;
logic                cts_cycle;
// __________________________________________________________
// _________________ ADDRESS TO KERNEL HEAD _________________ 

always_comb begin 
	cts_cycle    = i_enb_K || i_enb_M0 || i_enb_CN;
	o_end_kernel = (o_addr == LKA) && i_enb_K; 
end

always_ff @(posedge clk or negedge rst_n) begin
	if(~rst_n)               FKA <= '0;
	else if ( o_end_kernel ) FKA <= LKA + 1;
	else                     FKA <= FKA;
end
// __________________________________________________________
// _________________ ADDRESS TO KERNEL TAIL _________________ 

always_comb begin
	odd = (i_w[1:0]) ? 2'd3 : 2'd2;
	LKA = (i_w >> 2) + odd + FKA;
end
// __________________________________________________________
// _____________________ ADDRESS OUTPUT _____________________ 

always_ff @(posedge clk or negedge rst_n) begin
	if(~rst_n)            o_addr <= '0;
	else if ( cts_cycle ) o_addr <= o_addr + 1 + FKA; 
	else                  o_addr <= o_addr;
end



endmodule