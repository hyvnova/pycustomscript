if __name__ == "__main__":
    print(f"This file ({__name__}) should not be executed directly")
    exit(1)


from typing import Dict, Any, List, NoReturn
import tomli
from dataclasses import dataclass

# local modules
from .module_manager import process_modules, ModulePackageConfig

#  CONTANST ------------------------ <!>
DEFAULT_PACKAGE_MODULE_NAME = "origin"
CONFIG_FILE_NAME = "config.toml" # <!> this needs to change


@dataclass
class Field:
    """
    Descriptor object of a config file field
    """
    name: str
    description: str = ""
    type: Any = str
    required: bool = True


# field at config file which should have the list modules that will processed
MODULES_FIELD: Field = Field(
    name = "modules", 
    description = "List of Modules that import other CustomScript Modules. Prepares that listed modules to be imported",
    type = list
)

   
class Errors:
    
    @staticmethod
    def no_config() -> NoReturn:
        """
        When theres no config or not propre format on config file
        """
        print(
            "Error: No configuration found at:", CONFIG_FILE_NAME,
            "\n\t Make sure the config file has the proper format"
        )
        exit(1)
    
    @staticmethod
    def missing_field(field: Field) -> NoReturn:
        """
        Shows the information about the missing field.
        If `field.required` is `True` exits the program
        """
        
        print("Error > Missing Field:", field.name)
        
        print(
            f"\tField Description: {field.description} \n",
            f"\tField Type: {field.type}",
        )

        if field.required:
            exit(1)
            
    @staticmethod
    def wrong_field_type(field: Field) -> NoReturn:
        """
        Shows the right type expected at the field
        """
        
        print("Error > Wrong Field Type/Format:", field.name)
        
        print(
            f"\tExpected type: {field.type.__name__}\n",
            f"\tField Description: {field.description}"
        )
        
        

def get_field(field: Field, config_data: Dict[str, Any]) -> Any:
    """
    Gets a field value from `config_data` After: Checking it's existance and type
    """
    
    value: Any | None = config_data.get(field.name, None)
    
    # field doesnt exists
    if not value:
        Errors.missing_field(field) 
        
    # field has wrong type
    if not isinstance(value, field.type):
        Errors.wrong_field_type(field)
        
    return value
        
            
# main function     ------------------------------ <!> ------------------------------
def parse_config_file() -> Dict[str, Any]:
    """
    Parses/Processes config data and all fields in it.
    """
    
    # open and get contents of file
    config_data: Dict[str, Any] | None = tomli.load(open(CONFIG_FILE_NAME, "rb"))
    
    
    # check if file has contents and is a dict
    if not config_data or not isinstance(config_data, dict):
        print(
            "Error: No configuration found at:", CONFIG_FILE_NAME,
            "\n\t Make sure the config file has the proper format"
        )
        exit(1)
        
    # Parse modules
    modules: List[str] = get_field(MODULES_FIELD, config_data)
    
    process_modules(
        modules = modules,
        options = ModulePackageConfig().get_from(config_data)
    )
    
    return config_data

            
def get_from_config_file(key: str) -> Any | None:
    # open and get contents of file
    config_data: Dict[str, Any] | None = tomli.load(open(CONFIG_FILE_NAME, "rb"))
    
    # check if file has contents and is a dict
    if not config_data or not isinstance(config_data, dict):
        Errors.no_config()
        
    return config_data.get(key)
        
        
    