from asyncio import iscoroutinefunction

from backend.processor.girevance_extractor import ExtractGirevance
from backend.processor.mapping import Mapper
from backend.processor.processor import Processor
from backend.processor.response_generator import ResponseGenerator


class Pipeline:
    """Pipeline class for processing data."""

    def __init__(self, processors: list[Processor]) -> None:
        self.processors = processors

    async def run(self, data: dict) -> dict:
        """Run the pipeline."""
        for processor in self.processors:
            if iscoroutinefunction(processor.process):
                data = await processor.process(data)
            else:
                data = processor.process(data)
        return data


class InferencePipeline(Pipeline):
    """Pipeline class for selecting mfs."""

    def __init__(self) -> None:
        processors = [ExtractGirevance(), Mapper(), ResponseGenerator()]
        super().__init__(processors)
