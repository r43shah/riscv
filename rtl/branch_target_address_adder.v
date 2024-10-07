module branch_target_address_adder(
    input [31:0] immediate,
    input [31:0] pc,
    output [31:0] branch_target_address
);

    assign branch_target_address = pc + (immediate << 1);

endmodule