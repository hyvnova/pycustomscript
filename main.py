if __name__ != "__main__":
    print("THIS FILE SHOULD NOT BE IMPORTED, IS SUPPOSED TO BE RUNNED DIRECTLY")        
    exit(0)


import argparse

#local modules
from src.parseconfig import process_config_file


process_config_file()
exit(1)



# argument parse for taking and managing command from Command line
parser = argparse.ArgumentParser(
    prog = 'main.py',
    description = 'run, prepare or manage how the PyCustomScript interpreter works',
    epilog = 'check help.md to see the list a explanation of all commands'
)


parser.add_argument(
    "action", 
    default="run", 
    
    # COMMAND LIST  ---------------------------- <!> ---------------------------------
    choices=[
        "run"
    ]
)


# MANAGE COMMAND

args = parser.parse_args()

# RUN COMMAND
if args.action == "run":
    
    process_config_file()   
    
     