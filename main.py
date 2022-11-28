from patterns import patterns
import time


def run(raw_source: str, timeit: bool = False) -> None:
    """
    Runs the code given using CustomScript Sintax
    """
    if timeit:
        time_start = time.time()
        cpu_time_start = time.process_time()

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


    for pattern_handler in patterns:
        source = pattern_handler(source)

    # save source
    with open("__source.py", "w") as f:
        f.write(source)

    if timeit:
        time_end = time.time()
        cpu_time_end = time.process_time()

        print(f"TIME TAKEN TO BUILD SOURCE:\n\tTOTAL TIME: {time_end - time_start}\n\tCPU TIME: {cpu_time_end - cpu_time_start}")

    exec(source)
        
            