import os
import logging
import multiprocessing
from typing import Callable, List, Union
from subprocess import Popen, PIPE, TimeoutExpired


def popen(args: list) -> int:
    # insert command at beginning of list
    # not good for time complexity, but makes for more readable code
    #list(args).insert(0, command)
    

    with Popen(args, stdout=PIPE, stderr=PIPE, text=True) as proc:
        try:
            output, error = proc.communicate()
            trimmed_output, trimmed_error = output.strip(), error.strip()
        except TimeoutExpired:
            logging.debug('Process timed out')
            raise
        finally:
            if proc.poll() is None:
                proc.kill()
                output, error = proc.communicate()
                trimmed_output, trimmed_error = output.strip(), error.strip()
        if trimmed_output != []:
            logging.debug('output: ' + ''.join(trimmed_output))
        if trimmed_error != [] and len(trimmed_error) != 0:
            logging.debug(f"error: " + ''.join(trimmed_error))

        logging.debug(f'Function returned with code {proc.returncode}')
        return proc.returncode

def distribute_work(worker_function: Callable, command_args: List[str]) -> List[int]:
    pool = multiprocessing.Pool()
    logging.debug(f'Calling {worker_function.__name__} with {len(command_args)} arguments')
    ret_values = pool.map(worker_function, command_args)
    pool.close()
    pool.join()
    logging.debug(f'Pool has terminated with {len(ret_values)} return values')
    return ret_values

