from workflows import workflow_constants

class TooManyInputs(Exception):
    def __str__(self) -> str:
        return "Too many inputs were tried to be included for the tool."


class InputDoesNotExist(Exception):
    def __str__(self) -> str:
        return "Requested ID is not part of the tool's input."


class OutputDoesNotExist(Exception):
    def __str__(self) -> str:
        return "Requested ID is not part of the tool's output."
