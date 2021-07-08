import os
import logging
import multiprocessing
from typing import Callable, List, Union
from subprocess import Popen, PIPE, TimeoutExpired


def popen(command: str, args: list) -> int:
    # insert command at beginning of list
    # not good for time complexity, but makes for more readable code
    #list(args).insert(0, command)
    runnable_command = ['cmd' + command + args]

    with Popen(runnable_command, stdout=PIPE, stderr=PIPE, text=True) as proc:
        try:
            output, error = proc.communicate()
        except TimeoutExpired:
            logging.debug('Process timed out')
            raise
        finally:
            if proc.poll() is None:
                proc.kill()
                output, error = proc.communicate()
        if output != []:
            print('output: ' + ''.join(output.strip()))
        if error != []:
            print(f"error: " + ''.join(error.strip()))

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

