module register_file(
    input clk,
    input [4:0] read_reg1,
    input [4:0] read_reg2,
    input [4:0] write_reg,
    input [31:0] write_data,
    input read_write,
    output reg [31:0] read_data1,
    output reg [31:0] read_data2
);

    reg [31:0] reg_file [31:0];

    // we should write to reg_file at clock edge
    always@(posedge clk) begin
        if (read_write) begin
            reg_file[write_reg] <= write_data;
        end
    end

     //we should always be able to read rs1 and rs2
    assign read_data1 = reg_file[read_reg1];
    assign read_data2 = reg_file[read_reg2];

    initial begin
        $dumpfile("../vcd/register_file.vcd");
        $dumpvars(0,register_file);
    end

endmodule