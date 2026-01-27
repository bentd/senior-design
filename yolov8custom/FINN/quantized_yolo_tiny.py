import torch
import torch.nn as nn
from brevitas.nn import QuantConv2d, QuantReLU, QuantLinear, QuantMaxPool2d, QuantAvgPool2d
from brevitas.quant import Int8WeightPerTensorFixedPoint, Int8ActPerTensorFixedPoint

class QuantizedYOLOTiny(nn.Module):
    def __init__(self, num_classes=5, num_boxes=2):
        super().__init__()

        self.block1 = nn.Sequential(
            QuantConv2d(
                3, 16, kernel_size=3, stride=1, padding=1,
                weight_bit_width=8, weight_quant=Int8WeightPerTensorFixedPoint
            ),
            QuantReLU(
                bit_width=8,
                act_quant=Int8ActPerTensorFixedPoint,
                signed=False,
                narrow_range=False
            ),
            QuantMaxPool2d(kernel_size=2, stride=2)
        )

        self.block2 = nn.Sequential(
            QuantConv2d(
                16, 32, kernel_size=3, stride=1, padding=1,
                weight_bit_width=8, weight_quant=Int8WeightPerTensorFixedPoint
            ),
            QuantReLU(
                bit_width=8,
                act_quant=Int8ActPerTensorFixedPoint,
                signed=False,
                narrow_range=False
            ),
            QuantMaxPool2d(kernel_size=2, stride=2)
        )

        self.block3 = nn.Sequential(
            QuantConv2d(
                32, 64, kernel_size=3, stride=1, padding=1,
                weight_bit_width=8, weight_quant=Int8WeightPerTensorFixedPoint
            ),
            QuantReLU(
                bit_width=8,
                act_quant=Int8ActPerTensorFixedPoint,
                signed=False,
                narrow_range=False
            ),
            QuantAvgPool2d(kernel_size=4)
        )

        self.flatten = nn.Flatten()

        self.fc = QuantLinear(
            64 * 38 * 38,  # 640x640 input / 4 pooling downsamples → 640/2/2 = 160 → 160/4 = 40 (depends on exact padding, adjust if needed)
            num_boxes * (5 + num_classes),
            bias=True,
            weight_bit_width=8,
            weight_quant=Int8WeightPerTensorFixedPoint
        )

    def forward(self, x):
        x = self.block1(x)
        x = self.block2(x)
        x = self.block3(x)
        x = self.flatten(x)
        x = self.fc(x)
        return x

# ONNX export
if __name__ == "__main__":
    model = QuantizedYOLOTiny(num_classes=5, num_boxes=2)
    model.load_state_dict(torch.load("../models/quant_yolotiny_trained.pth"))
    model.eval()

    dummy_input = torch.randn(1, 3, 640, 640)  # Pre-quantized via transform
    torch.onnx.export(
        model,
        dummy_input,
        "../models/quant_yolotiny.onnx",
        input_names=["input"],
        output_names=["output"],
        export_params=True,
        opset_version=13,
        do_constant_folding=True
    )

    print("✅ Exported ONNX model to models/quant_yolotiny.onnx")
