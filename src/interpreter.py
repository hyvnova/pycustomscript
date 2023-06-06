if __name__ == "__main__":
    print(f"This file ({__name__}) should not be executed directly")
    exit(1)


from pathlib import Path
from os import system, mkdir, remove
from dataclasses import dataclass
import sys
from typing import List, Self
import ast

# local
from .patterns import patterns
from .custom_builtins import set_builtins

def move_path_up(path: Path, n: int) -> Path:
    """
    Returns the directory product of moving 1 dir "up" or "higher" `n` times
    """
    for _ in range(n):
        path = path.parent
        
    return path
    
           
def find_modules(file: Path, source_code: str) -> List[Path]:
    """
    Finds all modules being imported at `file` and returns them paths
    """
    
    tree = ast.parse(source_code)
    
    imports: List[Path] = []
    
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Import, ast.ImportFrom)):
            continue
        
        """
        node.names = List of aliases, "things being imported".
        node.level = level where the import is being done    
        

            level 0 (abs): from a package or module in the same dir    
            level 1 (abs) : import of a package or module in the same dir
            
            level n (relative) : from a module localted n dirs "higher" from the current path
        """        
                
        # import description
        level = getattr(node, "level", 1)
        # where import is being done at
        module: str = None
    
        
        # if is being imported from a module: "from module import ..."
        #                                           ^^^^^^
        if getattr(node, "module", None): 
            module = node.module
                        
        # if theres no module, then that means it is a: "import module"
        else:
            module = node.names[0].name
            
        # get module name 
        module = module.split(".")[0]
            
        # check if is importing a installed package, if so, skip it.
        if not module in sys.modules:
            
            # if is relative import
            if level >= 2:
                module_path = move_path_up(file, level-1)
                
            else:
                module_path = file.parent / module
            
            imports.append(module_path)

    return imports


@dataclass(slots=True)
class ModulePackageConfig:
    """
    Enum of options that affect the configutation of a package module creation.
    instanciating this object with no arguments creates the default creation config
    """
    quiet: bool = False
    

    def get_from(self, data: object | dict) -> Self:
        """
        Builds a `ModulePackageConfig` off a given `object` or `dict`.
        - THIS IS NOT A STATIC METHOD; INSTANCIATE THE OBJECT FISRT
        """
        
        data: dict = data if isinstance(data, dict) else data.__dict__
        
        for field, value in self.__dataclass_fields__.items():
            setattr(self, field, data.get(field, value))
            
        return self

    
def process_raw_source(
    file: Path | str, 
    output_file: str = "__source__/{filename}",
    quiet: bool = True
) ->  Path:
    """
    Takes the given `raw_source` and proecesses it to created a Python runable source file.
    Returns the source absolute path
    
    -  `quiet` : If `True` warnings won't be printed (Default: `False`)
    """
    
    if isinstance(file, str): 
        if not file.endswith(".py"):
            file += ".py"
            
        file = Path(file).absolute()

    # format output file name
    output_file: Path = file.parent / output_file.format(filename=Path(file).stem + ".py") 

    # clear __source__ dir
    if output_file.parent.name == "__source__":
        try:
            remove(output_file.parent)
            
        except OSError as e:
            if not quiet:
                print(f"WARNING: Could not clear {output_file.parent}\n\tError raised -> {e}\n")
            
        
    # create init at output file
    if not output_file.parent.exists():
        mkdir(output_file.parent)
        
        
    # file code
    raw_source = open(file, "r").read()
    
    # output source
    source = ""

    # clean lines
    for line in raw_source.split("\n"):

        # skip empty lines or comments
        if not line.strip() or line.startswith("#"):
            continue

        # remove commet
        if "#" in line:
            line = line.split("#")[0]

        source += line + "\n"

    # create __source__ folder if not exists
    if not output_file.parent.exists():
        mkdir(output_file.parent) 

    # apply patterns and save source
    with open(output_file, "w") as f:
        
        for pattern_handler in patterns:
            
            source = pattern_handler(source)
            
        f.write(source)
    
    return output_file.absolute()

def process_modules(main_file: Path, source_file: Path, options: ModulePackageConfig = ModulePackageConfig()) -> None:
    """
    Applies PyCS and custom_builtins to each file found at imports of `main_file`
    """
    modules = find_modules(main_file, open(source_file, "r").read())

    # Create package module (aka origin)          
    for module in modules:

        module_path: Path = module.parent / (module.stem + ".py")
        
        # creates the source module (PyCS file)
        source_module = process_raw_source(module_path.absolute(), quiet=options.quiet)
        
        # add custom builtins
        set_builtins(source_module)
       
def run(file: Path | str, options: ModulePackageConfig = ModulePackageConfig()) -> None:
    """
    Runs the code given using CustomScript Interpreter
    """
    if isinstance(file, str): 
        file = Path(file).absolute()

    # processes main file first because it needs to be ready before trying to find modules on it
    source_file: Path = process_raw_source(file, quiet=options.quiet)
        
    # Coverts files to pure python, Prepares custom builtins
    process_modules(file, source_file, options=options)
    
    # add custom builtins; added after to not interfire module search 
    set_builtins(source_file)

    # clear console
    if options.quiet:
        system("cls")
    
    print(f"\n\t[Running: {source_file}]\n")
        
    system(f"python {source_file}")
              

      
        
        


