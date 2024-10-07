module program_counter(
    input clk,
    input [31:0] pc_in,
    output reg [31:0] pc_out
);

    always @(posedge clk) begin
        pc_out <= pc_in; //pc_in is output of PC source mux
    end

endmodule