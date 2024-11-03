from torchvision.datasets import MNIST

from dataset.base.dataset_base import DatasetRegistry
from dataset.base.image_base_dataset import ImageDatasetBase

@DatasetRegistry.register
class MNistDataset(ImageDatasetBase):
    def __init__(self, root="./data/mnist", **kwargs):
        super().__init__(**kwargs)
        
    def __len__(self) -> int:
        raise NotImplementedError
    
    def __getitem__(self, idx) -> ?:
        raise NotImplementedError