module decoder(
    input clk,
    input [31:0] instruction,
    output [6:0] funct7,
    output [4:0] rs2,
    output [4:0] rs1,
    output [2:0] funct3,
    output [4:0] rd,
    output [6:0] opcode,
    output [31:0] imm
);

    //we will not support unsigned operations to keep things simpler
    
    always@(posedge clk) begin
        opcode = instruction[6:0];
        if (opcode[4:0] == 5'10111) begin //U type
            imm = {instruction[31:12],{12{1'b0}}};
            rd = instruction[11:7];
        end
        else if (opcode == 7'0110011) begin //R type
            funct7 = instruction[31:25];
            rs2 = instruction[24:20];
            rs1 = instruction[19:15];
            funct3 = instruction[14:12];
            rd = instruction[11:7];
        end
        else if (opcode[6:2] == 5b'00100 || opcode[6:2] == 5b'00000 || opcode[6:2] == 5'b11001) begin //I type
            if (instruction[14:12] == 0x1 & opcode[4]) begin
                imm = {{20{1'b0}},instruction[31:20]};
            end
            imm = instruction[31:20];
            rs1 = instruction[19:15];
            funct3 = instruction[14:12];
            rd = instruction[11:7];
        end
        else if (opcode == 7'b0100011) begin //S type
            imm = {20{instruction[31]},instruction[31:25],instruction[11:7]};
        end
        else if (opcode == 7'b1101111) begin //J type
            rd = instruction[11:7];
            imm = {{11{instruction[31]},instruction[31],instruction[19:12],instruction[11],instruction[10:1],1'b0}};
        end
        else if (opcode == 7'b1100011) begin
            funct3 = instruction[14:12];
            rs1 = instruction[19:15];
            rs2 = instruction[24:20];
            imm = {{19{instruction[31]}},instruction[31],instruction[7],instruction[30:25],instruction[11:8],1'b0};
        end
        else begin //opcode == 7'b1110011 ECALL
            //do nothing
        end

    end

endmodule