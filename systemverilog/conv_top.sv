`include "conv_control.sv"
`include "width_eval.sv"
`include "conv_addr.sv"
`include "conv_bank.sv"
`include "mem_model.sv"

module conv_top
#(
  parameter ADDR_WIDTH = 18,
  parameter K_PARAMS   = 16,
  parameter I_PARAMS   = 16,
  parameter KC_WIDTH   = 4,
  parameter IR_WIDTH   = 8,
  parameter OC_WIDTH   = 8,
  parameter WORD_WIDTH = 32,
  parameter BYTE_WIDTH = 8,
  parameter C_WIDTH    = 16,
  parameter N_WIDTH    = 8,
  parameter K_BYTES    = 9.0, 
  parameter M0_WIDTH   = 64
)(
  // ----------- CLOCK & RESET ----------
  input  logic clk,
  input  logic rst_n,
  // -------------- INPUTS -------------- 
  input  logic                i_begin,
  input  logic [I_PARAMS-1:0] i_iAxis,
  input  logic [K_PARAMS-1:0] i_kAxis,
  // ------------- OUTPUTS --------------
  output logic [I_PARAMS-1:0] o_iWidth,
  output logic [K_PARAMS-1:0] o_kWidth
);

localparam K_WIDTH = int'(K_BYTES * BYTE_WIDTH);
// __________________________________________________________
// ______________________ WIRES & NET _______________________ 

/* width & memory interface */
logic ready_mctr, valid_mctr;
logic ready_pctr, valid_pctr;
logic ready_peas, valid_peas;
logic ready_mem,  valid_mem, write_mem;
logic enb_axisreg, enb_peasent, enb_result, end_kernel;
logic [ADDR_WIDTH-1:0] LKA;

/* conv bank & memory interface */
logic enb_M0, enb_CN, enb_K , enb_win;
logic [K_WIDTH-1:0] kernel;
logic [M0_WIDTH-1:0] M0;
logic [N_WIDTH-1:0]  N;
logic [C_WIDTH-1:0]  C;
logic [WORD_WIDTH-1:0] data_mem;
logic [ADDR_WIDTH-1:0] addr_mem;

// ============================================================
//                       INSTANTIATIONS
// ============================================================
// __________________________________________________________
// ___________________ CONTROL SUBMODULE ____________________ 
 
conv_control control_FSM
(
  // INPUTS --------------------
  .clk           ( clk         ),
  .rst_n         ( rst_n       ),
  .i_begin       ( i_begin     ),
  .i_ready_pst   ( ready_peas  ),
  .i_valid_pst   ( valid_peas  ),
  .i_ready_mem   ( ready_mem   ),
  .i_valid_mem   ( valid_mem   ),
  .i_end_kernel  ( end_kernel  ),  
  // OUTPUTS -------------------
  .o_ready_pst   ( ready_pctr  ),
  .o_valid_pst   ( valid_pctr  ),
  .o_ready_mem   ( ready_mctr  ),
  .o_valid_mem   ( valid_mctr  ),
  .o_enb_axisreg ( enb_axisreg ),
  .o_enb_peasent ( enb_peasent ),
  .o_enb_result  ( enb_result ),
  .o_enb_M0      ( enb_M0      ),
  .o_enb_CN      ( enb_CN      ),
  .o_enb_K       ( enb_K       ),
  .o_enb_win     ( enb_win     )  
);
// __________________________________________________________
// ____________________ WEVAL SUBMODULE _____________________ 

width_eval
#(
  .K_PARAMS      ( K_PARAMS    ),
  .I_PARAMS      ( I_PARAMS    )
) weval_uut (
  .clk           ( clk         ),
  .rst_n         ( rst_n       ),
  .i_ready       ( ready_pctr  ),
  .i_valid       ( valid_pctr  ),
  .i_enb_axisreg ( enb_axisreg ),
  .i_enb_peasent ( enb_peasent ),
  .i_enb_result  ( enb_result  ),
  .i_iAxis       ( i_iAxis     ),
  .i_kAxis       ( i_kAxis     ),
  .o_iWidth      ( o_iWidth    ),
  .o_kWidth      ( o_kWidth    ),
  .o_ready       ( ready_peas  ),
  .o_valid       ( valid_peas  )
);
// __________________________________________________________
// ____________________ AEVAL SUBMODULE _____________________  

conv_addr #(
  .ADDR_WIDTH   ( ADDR_WIDTH ),
  .K_PARAMS     ( K_PARAMS   )
) 
aeval_uut 
(
  .clk          ( clk        ),
  .rst_n        ( rst_n      ),
  .i_enb_M0     ( enb_M0     ),
  .i_enb_CN     ( enb_CN     ),
  .i_enb_K      ( enb_K      ),
  .i_w          ( o_kWidth   ),
  .o_addr       ( addr_mem   ),
  .o_end_kernel ( end_kernel )

);
// __________________________________________________________
// _______________________ CONV BANK ________________________ 

conv_bank
#(
  .WORD_WIDTH  ( WORD_WIDTH ), 
  .BYTE_WIDTH  ( BYTE_WIDTH ), 
  .C_WIDTH     ( C_WIDTH    ), 
  .N_WIDTH     ( N_WIDTH    ), 
  .K_BYTES     ( K_BYTES    ), 
  .M0_WIDTH    ( M0_WIDTH   ),
  .K_OUT_WIDTH ( 8*9        )
) bank (
  .clk         ( clk        ),
  .rst_n       ( rst_n      ),  
  .i_enb_M0    ( enb_M0     ),
  .i_enb_CN    ( enb_CN     ),
  .i_enb_K     ( enb_K      ),
  .i_data      ( data_mem   ),
  .o_M0        ( M0         ),
  .o_N         ( N          ),
  .o_K         ( kernel     ),
  .o_C         ( C          )
);
// __________________________________________________________
// _____________________ MEMORY MODEL _______________________ 

mem_model
#(
  .WORD_WIDTH ( WORD_WIDTH ),
  .ADDR_WIDTH ( ADDR_WIDTH )
) mem (
  .clk        ( clk        ),
  .rst_n      ( rst_n      ),
  .i_ready    ( ready_mctr ),
  .i_valid    ( valid_mctr ),
  .i_write    ( 1'b0       ),
  .i_data     ( 0          ),
  .i_addr     ( addr_mem   ),
  .o_data     ( data_mem   ),
  .o_ready    ( ready_mem  ),
  .o_valid    ( valid_mem  ),
  .o_write    ( write_mem  )
);

endmodule