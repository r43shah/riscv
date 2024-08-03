module program_counter(
    input clk,
    input [31:0] pc,
    output reg [31:0] pc_out
);

    always @(posedge clk) begin
        pc_out <= pc + 4;
    end

initial begin
    $dumpfile("../vcd/program_counter.vcd");
    $dumpvars(0,program_counter);
end

endmodule