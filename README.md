# AVERON X1

An experimental GPU project built by a 14-year-old who loves technology and hardware engineering.

## About

AVERON X1 is my attempt to design and eventually build my own graphics processor. I'm starting with software simulations and gradually exploring actual GPU architecture and hardware design.

It's a long-term project, and I'm learning as I build.

## Current Progress
- First 3D triangle successfully rendered.
- Basic rendering pipeline implemented in the Python software rasterizer.
- Performance profiler added.
- First Verilog edge-function circuit written and compiled with Icarus Verilog 13.0.
- 8 selected edge-function test cases passed (8 passed, 0 failed).

## Verilog experiment

The first RTL experiment is a combinational edge-function unit in `03_Verilog/edge_function.v`.

- Inputs: six 16-bit signed coordinates.
- Output: one 34-bit signed result.
- Testbench: `03_Verilog/edge_function_tb.v`.
- Tested with basic values, negative coordinates and large results near the input limits.

The 8 tests passing is a good first check, not proof that every possible input works. Randomized testing is next.

## Status
Early development — no physical hardware yet.

More updates coming soon!
