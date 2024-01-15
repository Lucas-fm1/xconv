/*
$display("      11010   OO1O   0    1  1       1   ") 
$display("     01      O    O  11   0   0     0    ")
$display("     10      1    1  1 0  1    1   0     ")
$display("     11      O    1  0  1 0     1 0      ")
$display("      00111   O11O   0   10      1       ")
$display("    ===================================  ")
$display("           Image size:  (",x_inpt,",",y_inpt,")")
$display("           Kernel size: (",x_kern,",",y_kern,")")
$display("    ===================================  \n")
*/

module conv_counters 
#(
   parameter BYTE_WIDTH = 8,
   parameter WORD_WIDTH = 32,
   parameter ALGO_WIDTH = 4,
	parameter STRD_WIDTH = 4,
   parameter KERN_WIDTH = 3*3,

)(
	input  logic clk,    // Clock
	input  logic rst_n,  // Asynchronous reset active low
	// -------------- BUS INTERFACE -------------- 
	input  logic                  i_rvalid.bus,
	input  logic                  i_wvalid.bus,
	input  logic                  i_enb.bus,
	input  logic [WORD_WIDTH-1:0] i_data.bus,
	input  logic [STRD_WIDTH-1:0] i_stride.bus,
	input  logic [WORD_WIDTH-1:0] i_data.bus,
	// ------------- UNIT INTERFACE --------------
	input  logic [BYTE_WIDTH-1:0]   i_y.bus
	output logic [2*WORD_WIDTH-1:0] o_M0.bus,
	output logic [BYTE_WIDTH-1:0]   o_C.bus,
	output logic [BYTE_WIDTH-1:0]   o_N.bus,
	output logic [BYTE_WIDTH-1:0]   o_w.bus [0:KERN_WIDTH]
	output logic [BYTE_WIDTH-1:0]   o_x.bus [0:KERN_WIDTH]
	// ------------- CTRL INTERFACE --------------
	input  logic conv_CS,
	input  logic jump_KC,
	input  logic jump_IR,
	input  logic jump_OC,
	input  logic equal_cnts
);

logic [BYTE_WIDTH-1:0] mem_reg     [0:WORD_WIDTH/BYTE_WIDTH-1];
logic [WORD_WIDTH-1:0] M0_reg      [0:1];
logic [BYTE_WIDTH-1:0] window_sreg [0:KERN_WIDTH-1];
logic [BYTE_WIDTH-1:0] window_reg  [0:KERN_WIDTH-1];

// __________________________________________________________
// ____________________ MEMORY REGISTER _____________________ 

always @(posedge clk or negedge rst_n) begin
	if(~rst_n) begin // ------------------------------- RESET
		mem_reg <= 0;
	end else if(i_enb.bus) begin // ------------------- ENABLE
		if (i_rvalid.bus) begin // ------------------ READ WORD
			for (int mr1 = 0; mr1 < WORD_WIDTH/BYTE_WIDTH; mr1++)
				mem_reg[mr1] <= i_data.bus[BYTE_WIDTH*(mr1+1)-1:BYTE_WIDTH*mr1];
		end else begin 
			for (int mr2 = 0; mr2 < WORD_WIDTH/BYTE_WIDTH-1; mr2++)
				mem_reg[mr2] <= mem_reg[mr2+1]
			mem_reg[WORD_WIDTH/BYTE_WIDTH-1]  <= '0
		end
	end
end
// __________________________________________________________
// _________________ WINDOW SHIFT REGISTER __________________ 

always @(posedge clk or negedge rst_n) begin
	if(~rst_n) begin // ------------------------------- RESET
		window_sreg <= 0;
	end else if(i_enb.bus) begin // ------------------- ENABLE
		if (equal_cnts) begin // ------------------ READ WORD
			for (int mr1 = 0; mr1 < WORD_WIDTH/BYTE_WIDTH; mr1++)
				window_sreg[mr1] <= i_data.bus[BYTE_WIDTH*(mr1+1)-1:BYTE_WIDTH*mr1];
		end else begin 
			for (int mr2 = 0; mr2 < WORD_WIDTH/BYTE_WIDTH-1; mr2++)
				window_sreg[mr2] <= window_sreg[mr2+1]
			window_sreg[WORD_WIDTH/BYTE_WIDTH-1]  <= '0
		end
	end
end

endmodule