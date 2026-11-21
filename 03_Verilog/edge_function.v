
module edge_function (
    input  wire signed [15:0] x,
    input  wire signed [15:0] y,

    input  wire signed [15:0] x0,
    input  wire signed [15:0] y0,

    input  wire signed [15:0] x1,
    input  wire signed [15:0] y1,

    output wire signed [33:0] edge_value
);

    // Extend coordinates to 17 bits before subtraction.
    wire signed [16:0] sx  = {x[15], x};
    wire signed [16:0] sy  = {y[15], y};
    wire signed [16:0] sx0 = {x0[15], x0};
    wire signed [16:0] sy0 = {y0[15], y0};
    wire signed [16:0] sx1 = {x1[15], x1};
    wire signed [16:0] sy1 = {y1[15], y1};

    // Calculate coordinate differences.
    wire signed [16:0] dx = sx - sx0;
    wire signed [16:0] dy = sy1 - sy0;
    wire signed [16:0] py = sy - sy0;
    wire signed [16:0] px = sx1 - sx0;

    // Extend differences before multiplication.
    wire signed [33:0] dx_ext = {{17{dx[16]}}, dx};
    wire signed [33:0] dy_ext = {{17{dy[16]}}, dy};
    wire signed [33:0] py_ext = {{17{py[16]}}, py};
    wire signed [33:0] px_ext = {{17{px[16]}}, px};

    // Calculate the two multiplication terms.
    wire signed [33:0] term1 = dx_ext * dy_ext;
    wire signed [33:0] term2 = py_ext * px_ext;

    // Final edge function.
    assign edge_value = term1 - term2;

endmodule
