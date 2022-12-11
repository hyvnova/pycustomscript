if __name__ == "__main__":
    print(f"This file ({__name__}) should not be executed directly")
    exit(1)


import os
from typing import Dict, Any, List
import tomli
from dataclasses import dataclass
from pathlib import Path

# local modules
from .interpreter import process_raw_source
from .convert_to_cython import build_cython_module

#  CONTANST ------------------------ <!>
DEFAULT_PACKAGE_MODULE_NAME = "origin"
CONFIG_FILE_NAME = "config.toml" # <!> this needs to change



@dataclass
class Field:
    name: str
    description: str = ""
    type: str = str


# Field Names needed at config file; this is used for renaming
MODULE_IMPORT = Field(
    name = "ModuleImport", 
    description = "List of Modules that import other CustomScript Modules. Prepares that listed modules \
to be imported",

    type = dict.__name__
)



class Errors:
    
    @staticmethod
    def missing_field(field: Field) -> None:        
        print("Error > Missing Field:", field.name)
        
        print(
            f"\tField Description: {field.description} \n",
            f"\tField Type: {field.type}",
        )

        exit(1)

# main function     ------------------------------ <!> ------------------------------
def parse_config_file():
    # open and get contents of file
    config_data: Dict[str, Any] | None = tomli.load(open(CONFIG_FILE_NAME, "rb"))
    
    
    # check if file has contents and is a dict
    if not config_data or not isinstance(config_data, dict):
        print(
            "Error: No configuration found at:", CONFIG_FILE_NAME,
            "\n\t Make sure the config file has the proper format"
        )
        exit(1)
        
    # Parse module import
    if not (module_import := config_data.get(MODULE_IMPORT.name)):
        
        Errors.missing_field(module_import) # this ends the program
        
        
    name: str = module_import.get("name", DEFAULT_PACKAGE_MODULE_NAME)    
    modules: List[str] = module_import.get("modules", [])
    
    
    import_all: bool = module_import.get("import_all", False)
    
    # Create package module
    with open(name + ".py", "w", encoding="utf-8") as f:
             
        for module in modules:
    
            # at the processing, the .py is required to find the module as a file
            if not module.endswith(".py"):
                module += ".py"
            
            module_path = Path(module).absolute()
            module_name = module_path.name[:-3]
            
            # creates the source module 
            source_module = process_raw_source(module_path)
            
            #convert to cython
            if module_import.get("to_cython", True):
                
                # hold source module path to delete it when done   
                source_module_temp = source_module
                
                source_module = build_cython_module(
                    source_module_temp
                )
                
                # delete source module (PyCS module) to avoid conflict with cython module which has the same name
                os.remove(source_module_temp)
                del source_module_temp
                module_name = source_module.name.replace(".py", "")            
                
            # write imports at origin package
            f.write(
                f"from {source_module.parent.name} import {module_name}\n"
            )
            
def get_from_config_file(key: str) -> Any | None:
    # open and get contents of file
    config_data: Dict[str, Any] | None = tomli.load(open(CONFIG_FILE_NAME, "rb"))
    
    # check if file has contents and is a dict
    if not config_data or not isinstance(config_data, dict):
        print(
            "Error: No configuration found at:", CONFIG_FILE_NAME,
            "\n\t Make sure the config file has the proper format"
        )
        exit(1)
        
    return config_data.get(key)
        
        
    