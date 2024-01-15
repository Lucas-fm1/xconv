module reg_memdata
#(
  parameter WORD_WIDTH = 32,
  parameter BYTE_WIDTH = 8
)(
  // ----------- CLOCK & RESET ----------
  input  logic clk,
  input  logic rst_n,  
  // -------------- INPUTS -------------- 
  input  logic                  i_enb_prl,
  input  logic                  i_enb_byt,
  input  logic [WORD_WIDTH-1:0] i_data,
  // ------------- OUTPUTS --------------
  output logic [WORD_WIDTH-1:0] o_data_prl,
  output logic [BYTE_WIDTH-1:0] o_data_byt,
  output logic                  o_empty_reg
);

localparam SFT_WIDTH = WORD_WIDTH/BYTE_WIDTH;

logic [WORD_WIDTH-1:0] word_reg;
logic [SFT_WIDTH-1:0]  sft_reg;

always_ff @(posedge clk or negedge rst_n) begin
  if(~rst_n) begin
    word_reg <= 0;
  end else begin
    if(i_enb_prl) begin
      word_reg <= i_data;
    end else
      word_reg <= word_reg << 8;
  end
end 

always_ff @(posedge clk or negedge rst_n) begin
  if(~rst_n) begin
    sft_reg <= 1;
  end else begin
    if(i_enb_prl)      sft_reg <= 1;
    else if(i_enb_byt) sft_reg <= sft_reg << 1;
    else               sft_reg <= sft_reg;
  end
end

always_comb begin
  o_data_prl  = word_reg;
  o_data_byt  = (i_enb_byt) ? word_reg[WORD_WIDTH-1:WORD_WIDTH-BYTE_WIDTH] : '0;
  o_empty_reg = (sft_reg == 4'b1000);
end

endmodule