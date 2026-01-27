import torch
import torch.nn as nn
from brevitas.nn import QuantConv2d, QuantReLU, QuantLinear, QuantIdentity
from brevitas.quant import Int8WeightPerTensorFixedPoint, Int8ActPerTensorFixedPoint

class QuantizedYOLOTiny(nn.Module):
    def __init__(self, num_classes=2, num_boxes=2):  # Customize as needed
        super().__init__()
        
        self.quant_in = QuantIdentity(bit_width=8, act_quant=Int8ActPerTensorFixedPoint)

        self.block1 = nn.Sequential(
            QuantConv2d(3, 16, kernel_size=3, stride=1, padding=1,
                        weight_bit_width=8, weight_quant=Int8WeightPerTensorFixedPoint),
            QuantReLU(bit_width=8, act_quant=Int8ActPerTensorFixedPoint),
            nn.MaxPool2d(2)
        )

        self.block2 = nn.Sequential(
            QuantConv2d(16, 32, kernel_size=3, stride=1, padding=1,
                        weight_bit_width=8, weight_quant=Int8WeightPerTensorFixedPoint),
            QuantReLU(bit_width=8, act_quant=Int8ActPerTensorFixedPoint),
            nn.MaxPool2d(2)
        )

        self.block3 = nn.Sequential(
            QuantConv2d(32, 64, kernel_size=3, stride=1, padding=1,
                        weight_bit_width=8, weight_quant=Int8WeightPerTensorFixedPoint),
            QuantReLU(bit_width=8, act_quant=Int8ActPerTensorFixedPoint),
            nn.AdaptiveAvgPool2d((4, 4))
        )

        # Flatten and detect
        self.fc = QuantLinear(64 * 4 * 4, num_boxes * (5 + num_classes), 
                              bias=True, weight_bit_width=8, weight_quant=Int8WeightPerTensorFixedPoint)

    def forward(self, x):
        x = self.quant_in(x)
        x = self.block1(x)
        x = self.block2(x)
        x = self.block3(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x

# ONNX export
if __name__ == "__main__":
    model = QuantizedYOLOTiny(num_classes=5, num_boxes=2)
    model.load_state_dict(torch.load("../models/quant_yolotiny_trained.pth"))
    model.eval()

    dummy_input = torch.randn(1, 3, 640, 640)

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
