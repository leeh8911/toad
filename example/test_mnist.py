    """Mnist dataset으로 학습 파이프라인 구성하기
    """
import json

cfg = None
with open("./test_mnist_cfg.json", "r") as f:
    cfg = json.load(f)


print(cfg)
