module alu_source_mux(
    input [31:0] read_data_2,
    input [31:0] immediate,
    input alusrc,
    output reg [32:0] alu_operand
);

    always@(*) begin
        if (alusrc) begin
            alu_operand = immediate;
        end
        else begin 
            alu_operand = read_data_2;
        end
    end


endmodule