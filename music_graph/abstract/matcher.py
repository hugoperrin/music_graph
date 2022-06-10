from abc import abstractmethod


class AbstractMatcher:
    @abstractmethod
    def match(self, _id: str) -> str:
        ...
