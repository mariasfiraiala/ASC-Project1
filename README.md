Copyright 2024 Maria Sfiraiala (maria.sfiraiala@stud.acs.upb.ro)

# Le Stats Sportif - Project1

## Description

The project aims to implement a basic single master - multiple workers server, with the jobs being performed by the workers coming in form of queries on a massive `csv` file.

The logic of the implementation is divided between 3 major modules:

* `jobs`: functions and helpers to be used as jobs for every request

* `routes`: callback functions for `flask` requests

* `task_runner`: thread pool and worker classes

The workers were designed as a pool of threads, signaled by the shutdown method of the server when to exit; this was achieved with the help of an `Event` variable, followed by a check of the queue, in order to finish all remaining, running tasks.

### Data Structure

The `csv` file contains only 5 columns that interest us (_the columns are indexed starting with 0_):

1. the question (column no. 8)

1. the state (column no. 4)

1. the value (column no. 11)

1. the stratification category (column no. 30)

1. the stratification (column no. 31)

With these 5 pieces of information, we decided to create a 4 level nested dictionary as it follows:

```text
data
  ├── question_1
  |          ├── state_1
  |          |        ├── strat_cat_1
  |          |        |            ├── strat_1 : list_of_values
  |          |        |            ├── strat_2 : list_of_values
  |          |        |            .
  |          |        |            .
  |          |        |            .
  |          |        |            └── strat_n : list_of_values
  |          |        ├── strat_cat_2
  |          |        .
  |          |        .
  |          |        .
  |          |        └── strat_cat_n
  |          ├── state_2
  |          .
  |          .
  |          .
  |          └── state_n
  ├── question_2
  .
  .
  .
  └── question_n
```

This approach gives us better access time for queries based on question and state, and overall, a prettier and more accurate view of the actual data.

It also provides a very nice (lazy) manner of grabing all the values from the dictionary, based on different attributes:

```python
def data_values(data : dict) -> Iterable[float]:
    """Get values only from nested dictionary"""
    for v in data.values():
        if isinstance(v, dict):
            yield from data_values(v)
        elif isinstance(v, list):
            yield from v
        else:
            yield v
```

The nested dictionary is modified in the category based jobs due to the fact that the empty value for stratification and stratification category is not accepted:

```python
def without_nan(d : dict):
    """Remove entrie that don'y have stratification"""
    return {k: v for k, v in d.items() if k != ''}
```

### Synchronization

The jobs are stored in a `Queue` object, so the `put()`/`get()` methods are atomic.
We also wrapped the increment applied on the job id in a lock block, as multiple requests for routes can happen concurrently.
The last piece of synchronization was done for the `shutdown()` method: an `Event` object is set in order to inform the workers that they should exit, and they do just that, however, not before finishing executing all the tasks that were added before the shutdown request in the queue.

> **Note**: We added a timeout for the `get()` method of the queue, in order to break the blocking call in case we don't have anything to execute and we should exit.

### Git

Check out my `git` history [here](https://github.com/mariasfiraiala/ASC-Project1). 

## Observations Regarding the Project

I've managed to implement all the tasks of the project except for the `unittests` part.
I didn't have the time to dive into that, but I am still very happy with how the project turned out otherwise, as I believe that I am starting to write some very concise code.

Overall, it was fun, it made me familiarize myself with a plethora of subjects, while keeping it quite simple.
I just wish the task description was put into words better and the checker didn't have so many bugs.
I can tell that the team was rushed to publish the homework and that they didn't have the time to update the description.
**However, next time, please, for the love of God, update the ocw page too, don't make me browse the forum, fishing for all the notions that you didn't explain originally, but you are describing now.**
**This way, the homework page doesn't become obsolete and the students won't have to check out 3 different websites**

## Resources

* [stackoverflow.com - Best Way to Implement Nested Dictionaries](https://stackoverflow.com/a/19829714)

* [stackoverflow.com - Get All Values from Nested Dictionaries in Python](https://stackoverflow.com/a/31439438)

* [stackoverflow.com - How to Pythonically Yield All Values from a List](https://stackoverflow.com/a/18620655)

* [stackoverflow.com - What Is the Return Type Hint of a Generator Function](https://stackoverflow.com/a/43659081)

* [stackoverflow.com - Python Logging - AttributeError: module 'logging' has no attribute 'handlers'](https://stackoverflow.com/a/65814814)

* [stackoverflow.com - How to Log Source Filename and Line Number in Python](https://stackoverflow.com/a/533077)

* [stackoverflow.com - How to Keep Order of Sorted Dictionary Passed to jsonify() Function](https://stackoverflow.com/a/60780210)

* [docs.python.org - Queue](https://docs.python.org/3/library/queue.html)
