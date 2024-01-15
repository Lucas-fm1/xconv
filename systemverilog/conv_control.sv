
module conv_control 
(
  // ----------- CLOCK & RESET ----------
  input  logic clk,
  input  logic rst_n,
  // -------------- INPUTS --------------
  input  logic i_begin,
  input  logic i_ready_pst,
  input  logic i_valid_pst,
  input  logic i_ready_mem,
  input  logic i_valid_mem,
  input  logic i_end_kernel,
  // ------------- OUTPUTS --------------
  output logic o_ready_pst,
  output logic o_valid_pst,
  output logic o_ready_mem,
  output logic o_valid_mem,
  output logic o_enb_axisreg,
  output logic o_enb_peasent,
  output logic o_enb_result,
  output logic o_enb_M0,
  output logic o_enb_CN,
  output logic o_enb_K,
  output logic o_enb_win  
);
// __________________________________________________________
// ____________________ INTERNAL SIGNALS ____________________ 

typedef enum logic [2:0]
{
  IDLE,      // reset & wait to begin THE CONV
  EVAL_IW,   // evaluate input size
  EVAL_KW,   // evaluate kernel size
  READ_M01,  // get first 32b of M0
  READ_M02,  // get last 32b of M0
  READ_CN,   // get N and C
  READ_K     // get kernel 
} conv_state;

conv_state CS, NS;
// __________________________________________________________
// _________________ CURRENT STATE REGISTER _________________ 

always_ff@(posedge clk, negedge rst_n) begin
  if(!rst_n)
    CS <= IDLE;
  else
    CS <= NS;
end
// __________________________________________________________
// ____________________ NEXT STATE LOGIC ____________________ 

always_comb begin
  case(CS)
    IDLE: begin
      if(i_begin) NS = EVAL_IW;
      else        NS = IDLE;
    end
    EVAL_IW: begin  // -------- PREPARATION (PEASANT) 
      if(i_valid_pst) NS = EVAL_KW;
      else            NS = EVAL_IW;
    end
    EVAL_KW: begin
      if(i_valid_pst) NS = READ_M01;
      else            NS = EVAL_KW;
    end
    READ_M01: begin // -------- MEMORY CONST & KERNEL 
      if(i_valid_mem) NS = READ_M02;
      else            NS = READ_M01;
    end
    READ_M02: begin
      if(i_valid_mem) NS = READ_CN;
      else            NS = READ_M02;
    end
    READ_CN: begin
      if(i_valid_mem) NS = READ_K;
      else            NS = READ_CN;
    end
    READ_K: begin
      if(i_end_kernel) NS = IDLE; // <<<<<<========
      else             NS = READ_K;
    end
  endcase
end
// __________________________________________________________
// ______________________ STATE FLAGS _______________________ 

logic RV_mem_flag;

always_comb begin
  // ------------ WIDTH ------------ 
  o_enb_axisreg = i_begin && (CS == IDLE);
  o_enb_peasent = (CS == EVAL_KW);
  o_enb_result  = (CS < 3);
  o_ready_pst   = (CS == EVAL_KW || CS == EVAL_IW);
  o_valid_pst   = (CS == EVAL_KW || CS == EVAL_IW);
  RV_mem_flag   = i_valid_mem && i_ready_mem; 
  // ---------- PREPATION ----------
  o_ready_mem   = ~i_ready_mem && (CS == READ_K || CS == READ_M01 || CS == READ_M02 || CS == READ_CN);
  o_valid_mem   = ~i_valid_mem && (CS == READ_K || CS == READ_M01 || CS == READ_M02 || CS == READ_CN);
  o_enb_CN      = RV_mem_flag && (CS == READ_CN); 
  o_enb_K       = RV_mem_flag && (CS == READ_K);
  o_enb_M0      = RV_mem_flag && (CS == READ_M01 || CS == READ_M02);
end

endmodule
