# TODO-List
Simple command line TODO-List application for efficient management of tasks.
```bash
py todo.py --help
```
```
usage: todo.py [-h]
               {get-tasks,get-lists,new-task,new-list,remove-task,remove-list,mark-task,mark-list,edit-task,edit-list,search-tasks,search-lists}
               ...

Command line application for efficient management of tasks to be done.

options:
  -h, --help            show this help message and exit

Commands:
  {get-tasks,get-lists,new-task,new-list,remove-task,remove-list,mark-task,mark-list,edit-task,edit-list,search-tasks,search-lists}
                        Available commands
    get-tasks           List all tasks in a LIST.
    get-lists           List all todo LISTS in current working dir.
    new-task            Create a new TASK in a LIST.
    new-list            Create a new LIST.
    remove-task         Remove a TASK from a LIST.
    remove-list         Delete a LIST from current working dir.
    mark-task           Mark a TASK with a status.
    mark-list           Mark a LIST with a status.
    edit-task           Edit a TASK in a LIST.
    edit-list           Edit a LIST.
    search-tasks        Search for TASKs based on various criteria.
    search-lists        Search for LISTs based on various criteria.

END
```
