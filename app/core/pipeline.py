from abc import ABC, abstractmethod
from .media import MediaAsset

class BaseProcessor(ABC):
    @abstractmethod
    def process(self,asset: MediaAsset) -> MediaAsset:
        pass

class MetadataExtractorNode(BaseProcessor):
    def process(self,asset:MediaAsset) -> MediaAsset:
        asset.extract_metadata()
        return asset

class AIAnalyzerNode(BaseProcessor):
    def process(self,asset:MediaAsset) -> MediaAsset:
        print(f"Using AI Analyzer on{asset.filename}")
        asset.tags.append("outdoor")
        asset.tags.append("city")
        return asset

class MediaPipeline:
    def __init__(self):
        self.nodes = []

    def add_node(self, node:BaseProcessor):
        self.nodes.append(node)
    def execute(self, asset: MediaAsset) -> MediaAsset:
        for node in self.nodes:
            asset = node.process(asset)
        return asset