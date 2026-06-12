class InvalidFileFormat(Exception):
    pass

class EmptyDatasetError(ValueError):
    pass

class MissingColumnError(ValueError):
    pass

class DuplicateValueError(ValueError):
    pass

class DataValidationError(ValueError):
    pass