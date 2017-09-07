
class Source:
    """
    """

    def __init__(self, ):
        self.name = name
        self.mark = mark

    def init(self, vim, name, mark):
        self.__init__()


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

