module one_round (clk, state_in, key, state_out);
    input              clk;
    input      [127:0] state_in, key;
    output reg [127:0] state_out;
    wire       [7  :0] m00, m01, m02, m03,
                       m10, m11, m12, m13,
                       m20, m21, m22, m23,
                       m30, m31, m32, m33,
                       n00, n01, n02, n03,
                       n10, n11, n12, n13,
                       n20, n21, n22, n23,
                       n30, n31, n32, n33;                                         
    wire       [31:0]  s0,  s1,  s2,  s3,
                       k0,  k1,  k2,  k3, 
                       x0,  x1,  x2,  x3,
                       y0,  y1,  y2,  y3,    
                       z0,  z1,  z2,  z3,                       
                       p00, p01, p02, p03,
                       p10, p11, p12, p13,
                       p20, p21, p22, p23,
                       p30, p31, p32, p33;                                           
   

    assign {k0, k1, k2, k3} = key;

    // State Columns s0 ... s3
    assign {s0, s1, s2, s3} = state_in;  
    
    assign {m00, m01, m02, m03} = s0;   
//    assign m00 = s0[31:24];
//    assign m01 = s0[23:16];
//    assign m02 = s0[15:8];
//    assign m03 = s0[7:0];
    assign {m10, m11, m12, m13} = s1;   
    assign {m20, m21, m22, m23} = s2;   
    assign {m30, m31, m32, m33} = s3;   
    
    
    // inverse shift rows
    assign x0 = {m00, m31, m22, m13};
    assign x1 = {m10, m01, m32, m23};
    assign x2 = {m20, m11, m02, m33};
    assign x3 = {m30, m21, m12, m03};
    
    // inverse substitution
    iS4
        S4_1 (clk, x0, {n00, n31, n22, n13}),
        S4_2 (clk, x1, {n10, n01, n32, n23}),
        S4_3 (clk, x2, {n20, n11, n02, n33}),
        S4_4 (clk, x3, {n30, n21, n12, n03});
    
    // add round key
    assign y0 = {n00, n31, n22, n13} ^ k0;
    assign y1 = {n10, n01, n32, n23} ^ k1;
    assign y2 = {n20, n11, n02, n33} ^ k2;
    assign y3 = {n30, n21, n12, n03} ^ k3;                    
    
    // p00 .. p33 are bytes of the state (p01 column 0 row 1)
    // inverse mix column
    table_lookup
        t0 (clk, y0, p00, p31, p22, p13),
        t1 (clk, y1, p10, p01, p32, p23),
        t2 (clk, y2, p20, p11, p02, p33),
        t3 (clk, y3, p30, p21, p12, p03);

    // InverseMixColumns final XOR
    // TODO: verify reordering XOR operations for readability doesn't effect end result
    assign z0 = p00 ^ p31 ^ p22 ^ p13;
    assign z1 = p10 ^ p01 ^ p32 ^ p23;
    assign z2 = p20 ^ p11 ^ p02 ^ p33;
    assign z3 = p30 ^ p21 ^ p12 ^ p03;

    always @ (posedge clk)
        state_out <= {z0, z1, z2, z3};
endmodule

/* AES final round for every two clock cycles */
module final_round (clk, state_in, key_in, state_out);
    input              clk;
    input      [127:0] state_in;
    input      [127:0] key_in;
    output reg [127:0] state_out;
    wire [31:0] s0,  s1,  s2,  s3,
                z0,  z1,  z2,  z3,
                k0,  k1,  k2,  k3;
    wire [7:0]  p00, p01, p02, p03,
                p10, p11, p12, p13,
                p20, p21, p22, p23,
                p30, p31, p32, p33;
    
    assign {k0, k1, k2, k3} = key_in;
    
    assign {s0, s1, s2, s3} = state_in;

    iS4
        S4_1 (clk, s0, {p00, p01, p02, p03}),
        S4_2 (clk, s1, {p10, p11, p12, p13}),
        S4_3 (clk, s2, {p20, p21, p22, p23}),
        S4_4 (clk, s3, {p30, p31, p32, p33});
    
    assign z0 = {p00, p31, p22, p13} ^ k0;
    assign z1 = {p10, p01, p32, p23} ^ k1;
    assign z2 = {p20, p11, p02, p33} ^ k2;
    assign z3 = {p30, p21, p12, p03} ^ k3;    

    always @ (posedge clk)
        state_out <= {z0, z1, z2, z3};
endmodule

