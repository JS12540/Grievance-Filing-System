from asyncio import iscoroutinefunction

from processor.girevance_extractor import ExtractGirevance
from processor.mapping import Mapper
from processor.processor import Processor
from processor.response_generator import ResponseGenerator


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
