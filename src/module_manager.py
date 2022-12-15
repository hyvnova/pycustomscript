from dataclasses import dataclass
from pathlib import Path
from typing import List, Self

# local modules
from .interpreter import process_raw_source, convert_to_cython, set_builtins


@dataclass
class ModulePackageConfig:
    """
    Enum of options that affect the configutation of a package module creation.
    instanciating this object with no arguments creates the default creation config
    """
    custom_builtins: bool = False
    to_cython: bool = True
    

    def get_from(self, data: object | dict) -> Self:
        """
        Builds a `ModulePackageConfig` off a given `object` or `dict`.
        - THIS IS NOT A STATIC METHOD; INSTANCIATE THE OBJECT FISRT
        """
        
        data: dict = data if isinstance(data, dict) else data.__dict__
        
        for field, value in self.__dataclass_fields__.items():
            setattr(self, field, data.get(field, value))
            
        return self


def process_modules(modules: List[str], options: ModulePackageConfig = ModulePackageConfig()) -> None:
    """
    Creates a package module file which will be the origin point for imports of "processed"
    versions of each module given at `modules` 
    
    - `modules` : list of each module that will be "processed" and added to the origin
    """

    # Create package module (aka origin)             
    for module in modules:

        # at the processing, the .py is required to find the module as a file
        if not module.endswith(".py"):
            module += ".py"
        
        module_path = Path(module).absolute()
        
        # creates the source module 
        source_module = process_raw_source(module_path)
        
        # add custom builtins
        if options.custom_builtins:
            set_builtins(source_module)
        
        #convert to cython
        if options.to_cython:
            convert_to_cython(source_module)
            
            
        