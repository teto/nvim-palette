from abc import abstractmethod

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
    def name(self):
        return self.__class__.__name__


    @abstractmethod
    def serialize(self, _filter):
        """
        Should return serialized entries
        """
        pass

    @abstractmethod
    def map2command(self, line):
        """
        might rename to map_entry or anything
        """
        pass

