`define INSTRUCTION_ARRAY_SIZE 2048

module instruction_memory(
    input [31:0] read_address,
    output [31:0] instruction
);

    reg [7:0] instruction_array [`INSTRUCTION_ARRAY_SIZE-1:0]; //7:0 because instruction is byte addressable... maybe we could have made it word addressable?
    assign instruction = {instruction_array[read_address+3],instruction_array[read_address+2],
        instruction_array[read_address+1],instruction_array[read_address]};

endmodule