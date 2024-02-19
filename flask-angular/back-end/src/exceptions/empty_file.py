# @author Marildo Cesar 15/02/2024

class EmptyFileException(Exception):

    def __init__(self, description: str):
        self.description = description
        self.code = 422
