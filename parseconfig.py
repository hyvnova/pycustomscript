
from typing import Dict, Any
import yaml
from dataclasses import dataclass

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
    config_data: Dict[str | None, Any] | None = yaml.load(
        open(file, "r").read(), 
        yaml.Loader
    )
    
    # check if file has contents and is a dict
    if not config_data or not isinstance(config_data, dict):
        print(
            "Error: No configuration found at:", file,
            "\n\t Make sure the config file has the proper format"
        )
        exit(1)
        
    
    # Parse module import
    if not config_data.get(MODULE_IMPORT.name):
        Errors.MissingField(MODULE_IMPORT)
        

            
    print(config_data)