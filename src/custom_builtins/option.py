from typing import Any, Union

class Some:
    """
    Represents a value that can't be None.
    """
    def __init__(self, value: Any) -> None:
        self.value = value
    
    def __str__(self) -> str:
        return f"Some({self.value})"
    
    def __repr__(self) -> str:
        return f"Some({self.value})"
    
    def __bool__(self) -> bool:
        return True
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Some):
            return self.value == other.value
        return False
    
    def unwrap(self) -> Any:
        return self.value
    
    def expect(self, msg: str) -> Any:
        if self:
            return self.value
        raise ValueError(msg)
    

class Nothing:
    """
    Represents a value that can be None.
    """

    def __str__(self) -> str:
        return "Nothing"
    
    def __repr__(self) -> str:
        return "Nothing"
    
    def __bool__(self) -> bool:
        return False
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Nothing):
            return True
        return False
    
    @classmethod
    def __call__(cls) -> None:
        return cls

    @classmethod
    def unwrap(cls, self) -> Any:
        raise ValueError("Cannot unwrap a Nothing")
    
    @classmethod
    def expect(cls, msg: str = "Unexpected Nothing") -> Any:
        raise ValueError(msg)
    

Option = Union[Some, Nothing]