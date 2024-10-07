module branch_calculator(
    input [31:0] read_data_1,
    input [31:0] read_data_2,
    input branch_unsigned,
    output reg branch_equal,
    output reg branch_lessthan
);

    always@(*) begin
        if (read_data_1 == read_data_2) begin
            branch_equal = 1;
        end
        else begin
            branch_equal = 0;
        end

        if (branch_unsigned) begin
            if (read_data_1 < read_data_2) begin
                branch_lessthan = 1;
            end
            else;
        end
        else begin
            if ($signed(read_data_1) < $signed(read_data_2)) begin
                branch_lessthan = 1;
            end
        end
    end



endmodule