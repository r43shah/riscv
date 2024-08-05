`define MEMORY_SIZE 1000

module data_memory(
    input clk,
    input [31:0] addr,
    input [31:0] data_write,
    input mem_write,
    input mem_read,
    output reg [31:0] data_read
);

    reg [31:0] data_memory [`MEMORY_SIZE-1:0];

    always@(*) begin
        if (mem_read) begin
            data_read = data_memory[addr];
        end
    end

    always@(clk) begin
        if (mem_write) begin
            data_memory[addr] = data_write;
        end
    end

endmodule