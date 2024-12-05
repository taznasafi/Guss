import sys
import traceback


class GussExceptions(Exception):
    """ Common base class for all non-exit exceptions. """

    def __init__(self, message=None, *args):
        self.message = message
        super().__init__(self.message, *args)

    def __repr__(self):
        return self.message