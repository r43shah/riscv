module register_file(
    input clk,
    input [4:0] read_reg_1,
    input [4:0] read_reg_2,
    input [5:0] write_reg,
    input [31:0] write_data,
    output [31:0] read_data_1,
    output [31:0] read_data_2,
    input regwrite
);

    reg [31:0] reg_file [31:0];

    assign read_data_1 = reg_file[read_reg_1];
    assign read_data_2 = reg_file[read_reg_2];

    always @(posedge clk) begin
        if (regwrite) begin
            reg_file[write_reg] = write_data;
        end
        else;
    end

endmodule