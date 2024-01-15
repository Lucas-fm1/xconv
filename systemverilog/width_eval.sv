`include "peasant.sv"

module width_eval
#(
	parameter K_PARAMS = 16,
	parameter I_PARAMS = 16
)(
	// ----------- CLOCK & RESET ----------
	input  logic clk,
	input  logic rst_n,  
	// -------------- INPUTS -------------- 
	input  logic                i_ready,
	input  logic                i_valid,
	input  logic                i_enb_axisreg,
	input  logic                i_enb_peasent,
	input  logic                i_enb_result,
	input  logic [I_PARAMS-1:0] i_iAxis,
	input  logic [K_PARAMS-1:0] i_kAxis,
	// ------------- OUTPUTS --------------
	output logic [I_PARAMS-1:0] o_iWidth,
	output logic [K_PARAMS-1:0] o_kWidth,
	output logic                o_ready,
	output logic                o_valid
);

localparam KAXIS_WDT = K_PARAMS/2;
localparam IAXIS_WDT = I_PARAMS/2;
// _______________________________________________________________
// ___________________ INPUT & OUTPUT REGISTER ___________________ 

logic [K_PARAMS+I_PARAMS-1:0] axis_reg, result_reg;
logic [K_PARAMS-1:0] result;
logic [K_PARAMS-1:0] kAxis;
logic [I_PARAMS-1:0] iAxis;
logic                enb_result;

always @(posedge clk or negedge rst_n) begin
	if(~rst_n)				axis_reg <= '0;
	else if (i_enb_axisreg) axis_reg <= {i_iAxis,i_kAxis}; 
	else					axis_reg <= axis_reg; 
end
	//------------------------------------
always_comb enb_result = o_ready && o_valid && i_enb_result;
always @(posedge clk or negedge rst_n) begin
	if(~rst_n)
	    result_reg <= '0;
	else if(enb_result) begin 
		result_reg[I_PARAMS+K_PARAMS-1:K_PARAMS] <= result_reg[K_PARAMS-1:0];
		result_reg[K_PARAMS-1:0]        <= result;
	end else
		result_reg <= result_reg;
end
	//------------------------------------
always_comb begin
	o_iWidth = result_reg[I_PARAMS+K_PARAMS-1:K_PARAMS-1];
	o_kWidth = result_reg[K_PARAMS-1:0];
	iAxis    = axis_reg[I_PARAMS+K_PARAMS-1:K_PARAMS];
	kAxis    = axis_reg[K_PARAMS-1:0];
end

// _______________________________________________________________
// _________________________ PEASANT MUX _________________________ 

logic [I_PARAMS-1:0]  peasant_mux;
logic [IAXIS_WDT-1:0] A, B;

always_comb begin
	//---------- assignment -----------
	if (i_enb_peasent) peasant_mux = kAxis;
	else 			   peasant_mux = iAxis;
	//-------- peasant inputs --------- 
	A = peasant_mux[I_PARAMS-1:IAXIS_WDT]; // 8b
	B = peasant_mux[IAXIS_WDT-1:0];        // 8b
end
// _______________________________________________________________
// _______________________ PEASENT INSTANCE ______________________ 

peasant #(
    .NBITS  ( KAXIS_WDT )
) peas_instance (
	.clock  ( clk      ),
    .reset  ( rst_n     ),
	.iReady ( i_ready  ),
	.iValid ( i_valid  ),
	.A      ( A        ),
	.B      ( B        ),
	.result ( result   ),
	.oReady ( o_ready  ),
	.oValid ( o_valid  )
);

endmodule