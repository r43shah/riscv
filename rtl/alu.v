module alu(
    input clk,
    input [31:0] a,
    input [31:0] b,
    input [3:0] alu_sel,
    output [31:0] out,
);

    always@(*) begin
        case (alu_sel)
            4'b0000: begin
                out = a + b;
            end
            4'b0001: begin
                out = a - b;
            end
            4'b0010: begin
                out = a ^ b;
            end
            4'b0011: begin
                out = a | b;
            end
            4'b0100: begin
                out = a & b;
            end
            4'b0101: begin
                out = a << b;
            end
            4'b0110: begin
                out = a >> b;
            end
            4'b0111: begin
                out = a >>> b;
            end
            4'b1000: begin
                out = (a < b)? 1 : 0;
            end
            default: begin
                $fatal();
            end
        endcase
    end

endmodule


endmodule