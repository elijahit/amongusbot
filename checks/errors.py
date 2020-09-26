# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass


class CogNotLoadedError(Error):
    print('ciao')
    """Raised when the input value is too small"""
    pass

