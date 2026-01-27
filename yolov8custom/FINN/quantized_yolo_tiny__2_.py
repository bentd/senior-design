import torch
import torch.nn as nn
from brevitas.nn import QuantConv2d, QuantReLU, QuantHardTanh
from brevitas.core.quant import QuantType

class QuantizedYOLOv3Tiny(nn.Module):
    """
    YOLOv3-inspired quantized object detection model for 5 classes and bounding boxes.
    This model uses Brevitas quantized layers and is structured for FINN deployment on FPGA.
    Input:  RGB image tensor of shape (N, 3, 640, 640) with 8-bit quantized values (0-255 range).
    Output: Quantized feature map of shape (N, 30, 20, 20) encoding 3 anchors per cell with 5 classes + bbox.
            (Per anchor: 4 bbox offsets, 1 objectness, 5 class scores = 10 values, and 3 anchors -> 30 channels.)
    """

    def __init__(self):
        super(QuantizedYOLOv3Tiny, self).__init__()
        # Define quantization bit-widths for weights and activations
        # Using 2-bit weights (QuantType.INT for signed) and 2-bit activations for intermediate layers
        weight_bit_width = 2
        act_bit_width = 2

        # First convolution layer: 3 input channels -> 8 output channels, 3x3 kernel.
        # Using padding=1 to maintain 640x640 resolution. No bias for simplicity.
        self.conv1 = QuantConv2d(in_channels=3, out_channels=8, kernel_size=3, stride=1, padding=1, 
                                 bias=False, weight_bit_width=weight_bit_width, weight_quant_type=QuantType.INT)
        # Quantized ReLU activation (2-bit) after conv1
        self.act1 = QuantReLU(bit_width=act_bit_width)
        # 2x2 MaxPool to downsample (640 -> 320)
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)

        # Second conv: 8 -> 8 channels, 3x3
        self.conv2 = QuantConv2d(in_channels=8, out_channels=8, kernel_size=3, stride=1, padding=1, 
                                 bias=False, weight_bit_width=weight_bit_width, weight_quant_type=QuantType.INT)
        self.act2 = QuantReLU(bit_width=act_bit_width)
        # Downsample (320 -> 160)
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)

        # Third conv: 8 -> 16 channels, 3x3
        self.conv3 = QuantConv2d(in_channels=8, out_channels=16, kernel_size=3, stride=1, padding=1, 
                                 bias=False, weight_bit_width=weight_bit_width, weight_quant_type=QuantType.INT)
        self.act3 = QuantReLU(bit_width=act_bit_width)
        # Downsample (160 -> 80)
        self.pool3 = nn.MaxPool2d(kernel_size=2, stride=2)

        # Fourth conv: 16 -> 32 channels, 3x3
        self.conv4 = QuantConv2d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding=1, 
                                 bias=False, weight_bit_width=weight_bit_width, weight_quant_type=QuantType.INT)
        self.act4 = QuantReLU(bit_width=act_bit_width)
        # Downsample (80 -> 40)
        self.pool4 = nn.MaxPool2d(kernel_size=2, stride=2)

        # Fifth conv: 32 -> 56 channels, 3x3 
        # (56 is a reduced channel count ~1/5 of 256 from original tiny YOLO layer)
        self.conv5 = QuantConv2d(in_channels=32, out_channels=56, kernel_size=3, stride=1, padding=1, 
                                 bias=False, weight_bit_width=weight_bit_width, weight_quant_type=QuantType.INT)
        self.act5 = QuantReLU(bit_width=act_bit_width)
        # Downsample (40 -> 20)
        self.pool5 = nn.MaxPool2d(kernel_size=2, stride=2)

        # Sixth conv: 56 -> 104 channels, 3x3 
        # (104 ~1/5 of 512 from original; now feature map is 20x20)
        self.conv6 = QuantConv2d(in_channels=56, out_channels=104, kernel_size=3, stride=1, padding=1, 
                                 bias=False, weight_bit_width=weight_bit_width, weight_quant_type=QuantType.INT)
        self.act6 = QuantReLU(bit_width=act_bit_width)
        # (No pooling here; we keep 20x20 spatial size for output grid)

        # Seventh conv: 104 -> 208 channels, 3x3
        # This layer expands channel depth (similar to TinyYOLOv3 final layers) for more complex features
        self.conv7 = QuantConv2d(in_channels=104, out_channels=208, kernel_size=3, stride=1, padding=1, 
                                 bias=False, weight_bit_width=weight_bit_width, weight_quant_type=QuantType.INT)
        self.act7 = QuantReLU(bit_width=act_bit_width)

        # Eighth conv: 208 -> 56 channels, 1x1 
        # This 1x1 conv acts as a bottleneck to reduce channels (similar to Tiny YOLO's route layering)
        self.conv8 = QuantConv2d(in_channels=208, out_channels=56, kernel_size=1, stride=1, padding=0, 
                                 bias=False, weight_bit_width=weight_bit_width, weight_quant_type=QuantType.INT)
        self.act8 = QuantReLU(bit_width=act_bit_width)

        # Ninth conv: 56 -> 104 channels, 3x3 
        # Re-expand channels again after the bottleneck
        self.conv9 = QuantConv2d(in_channels=56, out_channels=104, kernel_size=3, stride=1, padding=1, 
                                 bias=False, weight_bit_width=weight_bit_width, weight_quant_type=QuantType.INT)
        self.act9 = QuantReLU(bit_width=act_bit_width)

        # Output conv: 104 -> 30 channels, 3x3 
        # 30 output channels correspond to 3 anchors * (5 classes + 1 objectness + 4 bbox coords).
        # We use a slightly higher bit-width for output for precision (e.g., 8-bit).
        self.conv_out = QuantConv2d(in_channels=104, out_channels=30, kernel_size=3, stride=1, padding=1, 
                                    bias=False, weight_bit_width=weight_bit_width, weight_quant_type=QuantType.INT)
        # Final activation: QuantHardTanh to clamp outputs to a finite range (0 to 1).
        # Using 8-bit for output activations (common for FINN output).
        self.act_out = QuantHardTanh(bit_width=8, min_val=0.0, max_val=1.0)
        # (HardTanh here approximates a sigmoid: it will saturate the output between 0 and 1 when de-quantized.)

    def forward(self, x):
        # Input x is expected to be 8-bit quantized (e.g., uint8 image). 
        # Pass through each layer sequentially:
        out = self.pool1(self.act1(self.conv1(x)))       # 640->320
        out = self.pool2(self.act2(self.conv2(out)))     # 320->160
        out = self.pool3(self.act3(self.conv3(out)))     # 160->80
        out = self.pool4(self.act4(self.conv4(out)))     # 80->40
        out = self.pool5(self.act5(self.conv5(out)))     # 40->20
        out = self.act6(self.conv6(out))                 # 20x20, 104 channels
        out = self.act7(self.conv7(out))                 # 20x20, 208 channels
        out = self.act8(self.conv8(out))                 # 20x20, 56 channels
        out = self.act9(self.conv9(out))                 # 20x20, 104 channels
        out = self.act_out(self.conv_out(out))           # 20x20, 30 channels (quantized output in [0,1] range)
        return out

# Example: create model and export (for illustration; actual export requires brevitas export utilities)
model = QuantizedYOLOv3Tiny()
print(model)
