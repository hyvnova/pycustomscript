if not __name__ == "__main__":
    print("THIS FILE SHOULD NOT BE IMPORTED, IS SUPPOSED TO BE RUNNED DIRECTLY")        
    exit(0)


import argparse

#local modules
from interpreter import run
from parseconfig import parse_config_file

# CONSTANT OF DEFAULT BEHAVIOR --------------------- <!> ----------------------------
CONFIG_FILE_NAME = "config.yaml" # <!> this needs to change



# argument parse for taking and managing command from Command line
parser = argparse.ArgumentParser(
    prog = 'main.py',
    description = 'run, prepare or manage how the PyCustomScript interpreter works',
    epilog = 'check help.md to see the list a explanation of all commands'
)


parser.add_argument("action", default="run", 
    # COMMAND LIST  ---------------------------- <!> ---------------------------------
    choices=[
        "run",
        "prepare"
    ]
)
parser.add_argument("-f", "--filename", required=False)



# MANAGE COMMAND

args = parser.parse_args()

# RUN COMMAND
if args.action == "run":
    
    if not args.filename:
        print("\t Missing -f/--filename argument: File that  will be run")
    
    run(args.filename)
    
# PREPARE COMMAND: Prepares the all modules listed in the config file
elif args.action == "prepare":
    
    parse_config_file(CONFIG_FILE_NAME)
    