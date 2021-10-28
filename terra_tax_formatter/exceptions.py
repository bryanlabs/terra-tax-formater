"""
Provides custom exception classes
"""

class ConverterCaughtError(Exception):
    """
    A very generic exception class, used as the Base to catch custom errors with
    specific messages
    """
    def __init__(self, message):
        self.message = message