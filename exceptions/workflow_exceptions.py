class ToolNotAvailable(Exception):
    def __str__(self) -> str:
        return "Requested tool is not implemented."


class ToolDoesNotExist(Exception):
    def __str__(self) -> str:
        return "Provided tool does not exist."


class RootCannotBeDeleted(Exception):
    def __str__(self) -> str:
        return "Root tool cannot be deleted."
