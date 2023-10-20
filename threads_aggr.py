
import threading
from queue import Queue
import time

# number of max thread can run at a time
MAX_T = 5

# ### Thread list validation
def validate_thread_list(thread_list):
    print(f'Validating thread list: {thread_list}')
    if type(thread_list) != list:
        print('Validation failed: thread_list var should be a list')
        return False

    if not thread_list:
        print('Validation failed: thread_list cannot be empty list')
        return False

    if len(thread_list) > MAX_T:
        print('Validation failed: thread limit exceeds')
        return False

    print('Threads validation success')
    return True


def start_process(thread_list):
    if not validate_thread_list(thread_list):
        raise Exception('Could not validate')
        
    print('Running threads parallelly..')
    print(f'Thread list: {thread_list}')
    # start all available threads
    for thread in thread_list:
        thread.start()

    # join the threads ran before to complete all threads executions
    for thread in thread_list:
        thread.join()


def aggregate_results(thread_queue):
    print('Aggregating thread results..')
    results_items_dict = {}
    # traverse queue until empty
    while not thread_queue.empty():
        # get value
        result_dict = thread_queue.get()
        for key, value in result_dict.items():
            results_items_dict[key] = value

    return results_items_dict


def func1(param1):
    print('Func1 started..waiting 2 sec')
    time.sleep(2)
    print('Func1 complete')
    return f'func1 val: {param1}'


def func2(param1, param2):
    print('Func2 started..waiting 5 sec')
    time.sleep(5)
    print('Func2 complete')
    return f'func2 val: {param1}, {param2}'


def interface_function(param1, param2, ops):
    # all threads will run these function
    # Call different function based on parameter ops
    if ops == 'func1':
        return {'func1': func1(param1)}

    if ops == 'func2':
        return {'func2': func2(param1, param2)}


ops_list = ['func1', 'func2']

# initialize thread queue
thread_que = Queue()
thread_list = []  # contains a list of threads

for ops in ops_list:
    # make a thread object and insert into thread list
    thread = threading.Thread(
        target = lambda que, param1, param2, param3: que.put(interface_function(param1, param2, param3)),
        args = (thread_que, 'value1', 'value2', ops)
    )
    thread_list.append(thread)

# run all available threads in thread list
start_process(thread_list)

# aggregate results
results_items_dict = aggregate_results(thread_que)
print(f'Aggregated results: {results_items_dict}')
