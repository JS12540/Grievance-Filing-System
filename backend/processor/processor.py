from abc import abstractmethod


class Processor:
    """An abstract method that takes in a dictionary of data and returns a dictionary.
    This method is intended to be overridden by subclasses and should be implemented
    to process the input data and return the processed data.

    Parameters:
        data (dict): The input data to be processed.

    Returns:
        dict: The processed data.
    """  # noqa: D205

    @abstractmethod
    async def process(self, data: dict) -> dict:
        """Asynchronously transforms the input data based on defined processing rules.

        This method should be overridden to include specific logic that manipulates the
        data, potentially involving I/O operations such as fetching, modifying, and
        returning data. It ensures that the data handling is performed asynchronously
        to optimize performance.

        Args:
            data: An instance of type dict, representing the data to be processed.

        Returns:
            An instance of type dict, representing the transformed or processed data.
        """
        pass
