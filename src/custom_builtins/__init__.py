
from pathlib import Path
from os import listdir
from importlib.machinery import SourceFileLoader

HERE = Path(__file__).parent

CUSTOM_BUILTINS_MODULE_NAME: str = "__custom_builtins__.py"

def set_builtins(source_file: Path) -> None:
    
    with open(source_file, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        
        f.write("from importlib.machinery import SourceFileLoader\n")
        
        for file in listdir(HERE):
            
            if file.startswith("_"): # skip files that startswith "_"
                continue

            name = file[:-3]

            f.write(f"""
{name} = getattr(
    SourceFileLoader(
        "{name}", # module name
        r"{(HERE / Path(file).name).absolute()}"
    ).load_module(), # import buildin module by path
    
    "{name}",
    globals()["__builtins__"].get("{name}") # default value
)

""" + content)
        
