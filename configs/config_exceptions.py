class ConfigClassIsMissing(Exception):
    def __str__(self) -> str:
        return "Config class is missing for this tool."
