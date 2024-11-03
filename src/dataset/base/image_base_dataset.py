from torch.utils.data import Dataset

from core.registry import REGISTRY_FACTORY
from dataset_base import DatasetRegistry


class ImageDatasetBase(Dataset):
    def __init__(self, **kwargs):
        pass
