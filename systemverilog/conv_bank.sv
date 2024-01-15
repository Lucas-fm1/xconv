module conv_bank
#(
	parameter WORD_WIDTH  = 32,
	parameter BYTE_WIDTH  = 8,
	parameter C_WIDTH     = 16,
	parameter N_WIDTH     = 8,
	parameter K_BYTES     = 9.0,  // kernel width at the biggest layer
	parameter M0_WIDTH    = WORD_WIDTH * 2,
	parameter K_OUT_WIDTH = K_BYTES * BYTE_WIDTH
)(
	// ----------- CLOCK & RESET ----------
	input  logic clk,
	input  logic rst_n,  
	// -------------- INPUTS --------------
	input  logic                  i_enb_M0,
	input  logic                  i_enb_CN,
	input  logic                  i_enb_K,
	input  logic [WORD_WIDTH-1:0] i_data,
	// ------------- OUTPUTS --------------
	output logic [M0_WIDTH-1:0]    o_M0,
	output logic [N_WIDTH-1:0]     o_N,
	output logic [K_OUT_WIDTH-1:0] o_K,
	output logic [C_WIDTH-1:0]     o_C
);

localparam CN_WIDTH    = C_WIDTH + N_WIDTH;
localparam K_WORDS     = int'($ceil(K_BYTES/4)); 
localparam K_REG_WIDTH = K_WORDS * WORD_WIDTH;

// __________________________________________________________
// ____________________ INTERNAL SIGNALS ____________________

logic [M0_WIDTH-1:0]    M0_reg;
logic [CN_WIDTH-1:0]    CN_reg;
logic [K_REG_WIDTH-1:0] K_reg;
// __________________________________________________________
// ______________________ M0 REGISTER _______________________

always @(posedge clk or negedge rst_n) begin
	if(~rst_n)
	  M0_reg <= '0;
	else if(i_enb_M0) begin 
		M0_reg[M0_WIDTH-1:WORD_WIDTH] <= M0_reg[WORD_WIDTH-1:0];
		M0_reg[WORD_WIDTH-1:0]        <= i_data;
	end else
		M0_reg <= M0_reg;
end
// __________________________________________________________
// ______________________ CN REGISTER _______________________

always @(posedge clk or negedge rst_n) begin
	if(~rst_n)        CN_reg <= '0;
	else if(i_enb_CN) CN_reg <= i_data; 
	else              CN_reg <= CN_reg;
end
// __________________________________________________________
// ______________________ KC REGISTER _______________________

always @(posedge clk or negedge rst_n) begin
	if(~rst_n)
		K_reg <= '0;
	else if(i_enb_K) begin
		K_reg[K_REG_WIDTH-1:WORD_WIDTH] <= K_reg[WORD_WIDTH-1:0];
		K_reg[WORD_WIDTH-1:0]           <= i_data;
	end else
		K_reg <= K_reg;
end

always_comb begin
	o_M0 = M0_reg;
	o_N  = CN_reg[N_WIDTH-1:0];
	o_C  = CN_reg[CN_WIDTH-1:N_WIDTH];
	o_K  = K_reg[K_REG_WIDTH-1:K_REG_WIDTH-K_OUT_WIDTH];
end

endmodule