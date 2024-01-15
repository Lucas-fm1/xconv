module reg_window
#(
  parameter BYTE_WIDTH = 8,
  parameter K_BYTES    = 9,
  parameter WIND_WIDTH = 8 * 9
)(
  // ----------- CLOCK & RESET ----------
  input  logic clk,
  input  logic rst_n,  
  // -------------- INPUTS -------------- 
  input  logic                  i_equal_addr,
  input  logic                  i_enb_byt,
  input  logic [BYTE_WIDTH-1:0] i_data_byt,
  // ------------- OUTPUTS --------------
  output logic [WIND_WIDTH-1:0] o_window
);
// __________________________________________________________
// ____________________ INTERNAL SIGNALS ____________________

logic [WIND_WIDTH-1:0] window;
logic                  valid_byt;
// __________________________________________________________
// ______________________ WINDOW ARRAY ______________________

always_comb valid_byt = i_equal_addr && i_enb_byt; 

always_ff @(posedge clk or negedge rst_n) begin
  if(~rst_n) begin
    window <= '0;
  end else begin
    if(valid_byt) begin
      window[WIND_WIDTH-1:BYTE_WIDTH] <= window[WIND_WIDTH-BYTE_WIDTH-1:0];
      window[BYTE_WIDTH-1:0]          <= i_data_byt;
    end else
      window <= window;
  end
end 
// __________________________________________________________
// ___________________ OUTPUTS ASSIGNMENT ___________________

always_comb o_window = window;

endmodule