`define MEMORY_SIZE 1000

module data_memory(
    input clk,
    input [31:0] addr,
    input [31:0] data_write,
    input enable,
    input read_write,
    output reg [31:0] data_read
);

    reg [31:0] data_memory_array [`MEMORY_SIZE-1:0];

    always@(*) begin
        if (enable & !read_write) begin
            data_read = data_memory_array[addr];
        end
    end

    always@(posedge clk) begin
        if (enable & read_write) begin
            data_memory_array[addr] = data_write;
        end
    end

    initial begin
        $dumpfile("../vcd/data_memory.vcd");
        $dumpvars(0,data_memory);
    end


endmodule