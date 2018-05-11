from abc import abstractmethod
from typing import List

class Source:
    """
    """

    def __init__(self, vim, *args, **kwargs ):
        # self._mark = ""
        self.vim = vim
        # super.init()

    # def init(self, vim, ):
        # pass


    @property
    def mark(self):
        return self.name

    @property
    @abstractmethod
    def name(self):
        return self.__class__.__name__

    @abstractmethod
    def serialize(self, _filter) -> List:
        """
        Should return serialized entries, i.e. as a list ?
        Get 
        """
        pass

    @abstractmethod
    def map2command(self, line) -> str:
        """
        might rename to map_entry or anything
        map 
        """
        pass

