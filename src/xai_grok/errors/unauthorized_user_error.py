import abc


class UnauthorizedUserError(Exception, abc.ABC):

    @abc.abstractmethod
    def __init__(self, message: str):
        super().__init__(message)
