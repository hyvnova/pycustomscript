from typing import Any, List, Self


class list(list):
    
    def split_at(self, index: int, include_index: bool = False) -> list:
        """
        Splits the list at the given index
        If `incldue_index` is true, then the item at `index` will be included at the first half of the split
        
        Example
        ```py
        [1,2,3,4,5].split_at(2) # [[1,2], [4,5]]
        """
        
        new = [
            self[:index + int(include_index)],
            self[index+1:]
        ]
        
        return new
    
    def split(self, item: Any) -> list:
        """
        Splits the list at the indexes where `item` is at
        
        Example
        ```py
        [1,2,3,4,3,2,1].split(3) # [[1, 2], [4], [2, 1]]
        """
        
        indexes: List[int] = [
            index
            for index, iteration_item in enumerate(self)
            if iteration_item == item
        ]

        new: List[int] = []
        
        for index, split_index in enumerate(indexes):
            
            # where the split starts
            start = (indexes[index-1] + 1) if index > 0 else 0
            
            new.append(
                self[start:split_index]
            )
        
        # append slice after last split index
        new.append(self[indexes[-1]+1:len(self)])
        
        return new
    
print(list((1,2,3,4,3,2,1)).split(3))
    

    
    