
from typing import Dict, Any, List
import tomli
from dataclasses import dataclass
from pathlib import Path

# local modules
from .interpreter import prepare_module

#  CONTANST ------------------------ <!>
DEFAULT_PACKAGE_MODULE_NAME = "origin"


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
    
    def MissingField(field: Field) -> None:
        print("Error > Missing Field:", MODULE_IMPORT.name)
        
        print(
            f"\tField Description: {MODULE_IMPORT.description} \n",
            f"\tField Type: {MODULE_IMPORT.type}",
        )

        exit(1)
        

# main function     ------------------------------ <!> ------------------------------
def parse_config_file(file: str):
    # open and get contents of file
    config_data: Dict[str, Any] | None = tomli.load(open(file, "rb"))
    
    
    # check if file has contents and is a dict
    if not config_data or not isinstance(config_data, dict):
        print(
            "Error: No configuration found at:", file,
            "\n\t Make sure the config file has the proper format"
        )
        exit(1)
        
    
    # Parse module import
    if not (module_import := config_data.get(MODULE_IMPORT.name)):
        Errors.MissingField(MODULE_IMPORT)
        
    name: str = module_import.get("name", DEFAULT_PACKAGE_MODULE_NAME)    
    modules: List[str] = module_import.get("modules", [])
    
    
    # Create package module
    with open(name + ".py", "w", encoding="utf-8") as f:
             
        for module_name in modules:
            
            # creates the source module and gets the name of it
            source_module_name = Path(prepare_module(module_name + ".py").__file__).name[:-3]
            
            f.write(
                f"import {source_module_name} as {module_name}\n"
            )