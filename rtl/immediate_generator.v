module immediate_generator(
    input [31:0] instruction,
    output reg [31:0] immediate
);

    wire [6:0] opcode;
    assign opcode = instruction[6:0];

    always@(*) begin
        case (opcode)
            7'b00x_0011: immediate = instruction[31:20]; //I-type
            7'b110_0111: immediate = instruction[31:20]; //also I-type
            7'b010_0011: immediate = {instruction[31:25],instruction[11:7]}; //S-type
            7'b110_0011: immediate = {instruction[31],instruction[7],instruction[30:25],instruction[11:8]}; //B-type
            7'b110_1111: immediate = {instruction[31],instruction[19:12],instruction[20],instruction[30:21]}; //J-type
        endcase
    end

endmodule