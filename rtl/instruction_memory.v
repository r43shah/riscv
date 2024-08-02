`define INSTRUCTION_SIZE 16

module instruction_memory(
    input clk,
    input [31:0] read_address,
    output reg [31:0] instruction,
    input read_enable
);

    reg [7:0] inst_array [`INSTRUCTION_SIZE-1: 0];

    always @(posedge clk) begin
        if (read_enable) begin
            instruction <= {inst_array[read_address+3], inst_array[read_address+2], 
                            inst_array[read_address+1], inst_array[read_address]};
        end
    end

initial begin
    $dumpfile("../vcd/output.vcd");
    $dumpvars(0,instruction_memory);
end

endmodule