class WrapperAPIException(Exception):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.args}"
