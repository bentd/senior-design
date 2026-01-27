import torch
import torch.nn as nn
from brevitas.nn import QuantConv2d, QuantLinear, QuantReLU, QuantIdentity
from brevitas.quant import Int8WeightPerTensorFixedPoint, Int8ActPerTensorFixedPoint

# Load the saved YOLOv8 backbone model
float_model = torch.load("torch_model.pth")

# Define a dummy input
dummy_input = torch.randn(1, 3, 640, 640)

# Wrap layers manually (for demo, you must expand for all layers in YOLOv8)
class QuantizedYOLO(nn.Module):
    def __init__(self):
        super().__init__()
        self.quant = QuantIdentity(bit_width=8, act_quant=Int8ActPerTensorFixedPoint)
        self.conv1 = QuantConv2d(3, 32, 3, stride=1, padding=1,
                                 weight_bit_width=8, weight_quant=Int8WeightPerTensorFixedPoint)
        self.relu = QuantReLU(bit_width=8, act_quant=Int8ActPerTensorFixedPoint)
        self.pool = nn.MaxPool2d(2)

        # NOTE: This is only an example layer. You must convert all YOLOv8 layers similarly.
    
    def forward(self, x):
        x = self.quant(x)
        x = self.conv1(x)
        x = self.relu(x)
        x = self.pool(x)
        return x

quant_model = QuantizedYOLO()

# Export to ONNX
torch.onnx.export(
    quant_model,
    dummy_input,
    "quant_yolo.onnx",
    input_names=['input'],
    output_names=['output'],
    export_params=True,
    opset_version=13,
    do_constant_folding=True
)

print("✅ Exported Brevitas quantized ONNX model: quant_yolo.onnx")
