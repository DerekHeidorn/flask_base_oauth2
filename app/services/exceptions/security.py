
class AppAccessDeniedException(Exception):
    _exception_msg = None

    def __init__(self, exception_msg):
        self._exception_msg = exception_msg

    def __repr__(self):
        return str(self._exception_msg)
