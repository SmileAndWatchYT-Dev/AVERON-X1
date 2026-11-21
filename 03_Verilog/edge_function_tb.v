
`timescale 1ns/1ps

module edge_function_tb;

    reg signed [15:0] x, y;
    reg signed [15:0] x0, y0;
    reg signed [15:0] x1, y1;

    wire signed [33:0] edge_value;

    edge_function uut (
        .x(x), .y(y),
        .x0(x0), .y0(y0),
        .x1(x1), .y1(y1),
        .edge_value(edge_value)
    );

    integer passed = 0;
    integer failed = 0;

    initial begin
        $display("AVERON X1 - Edge Function Stress Test");
        $display("-------------------------------------");

        // Test 1: Basic calculation
        x = 1; y = 2;
        x0 = 0; y0 = 0;
        x1 = 4; y1 = 0;
        #10;
        if (edge_value == -8) begin
            $display("Test 1: PASS");
            passed = passed + 1;
        end else begin
            $display("Test 1: FAIL - Got %0d", edge_value);
            failed = failed + 1;
        end

        // Test 2: Point on the edge
        x = 2; y = 0;
        x0 = 0; y0 = 0;
        x1 = 4; y1 = 0;
        #10;
        if (edge_value == 0) begin
            $display("Test 2: PASS");
            passed = passed + 1;
        end else begin
            $display("Test 2: FAIL - Got %0d", edge_value);
            failed = failed + 1;
        end

        // Test 3: Positive result
        x = 1; y = 1;
        x0 = 0; y0 = 0;
        x1 = 0; y1 = 4;
        #10;
        if (edge_value == 4) begin
            $display("Test 3: PASS");
            passed = passed + 1;
        end else begin
            $display("Test 3: FAIL - Got %0d", edge_value);
            failed = failed + 1;
        end

        // Test 4: Negative coordinates
        x = -1; y = -2;
        x0 = -4; y0 = -3;
        x1 = 2; y1 = -3;
        #10;
        if (edge_value == -6) begin
            $display("Test 4: PASS");
            passed = passed + 1;
        end else begin
            $display("Test 4: FAIL - Got %0d", edge_value);
            failed = failed + 1;
        end

        // Test 5: Negative differences
        x = 3; y = 4;
        x0 = 5; y0 = 5;
        x1 = 1; y1 = 2;
        #10;
        if (edge_value == 2) begin
            $display("Test 5: PASS");
            passed = passed + 1;
        end else begin
            $display("Test 5: FAIL - Got %0d", edge_value);
            failed = failed + 1;
        end

        // Test 6: Large coordinates
        x = 30000; y = 30000;
        x0 = -30000; y0 = -30000;
        x1 = 30000; y1 = -30000;
        #10;
        if (edge_value == -3600000000) begin
            $display("Test 6: PASS");
            passed = passed + 1;
        end else begin
            $display("Test 6: FAIL - Got %0d", edge_value);
            failed = failed + 1;
        end

        // Test 7: Maximum positive result
        x = 32767; y = -32768;
        x0 = -32768; y0 = 32767;
        x1 = 32767; y1 = 32767;
        #10;
        if (edge_value == 34'sd4294836225) begin
            $display("Test 7: PASS");
            passed = passed + 1;
        end else begin
            $display("Test 7: FAIL - Got %0d", edge_value);
            failed = failed + 1;
        end

        // Test 8: Large negative result
        x = -32768; y = 32767;
        x0 = -32768; y0 = -32768;
        x1 = 32767; y1 = -32768;
        #10;
        if (edge_value == -34'sd4294836225) begin
            $display("Test 8: PASS");
            passed = passed + 1;
        end else begin
            $display("Test 8: FAIL - Got %0d", edge_value);
            failed = failed + 1;
        end

        $display("-------------------------------------");
        $display("PASSED: %0d", passed);
        $display("FAILED: %0d", failed);

        if (failed == 0)
            $display("ALL TESTS PASSED!");
        else
            $display("SOME TESTS FAILED!");

        $finish;
    end

endmodule
