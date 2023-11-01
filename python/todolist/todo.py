from os import path
import argparse
import json

parser = argparse.ArgumentParser(prog='todo.py', description="Command line application for efficient management of tasks to be done.", epilog='END')

command_parser = parser.add_subparsers(dest='command', help='Available commands', title='Commands')


# list tasks
list_task_parser = command_parser.add_parser('get-tasks', help='List all tasks in a LIST.')
list_task_parser.add_argument('listid', type=int, help='ID of LIST to display TASKS from.')

# list todolist
list_list_parser = command_parser.add_parser('get-lists', help='List all todo LISTS in current working dir.')

# new task
new_task_parser = command_parser.add_parser('new-task', help='Create a new TASK in a LIST.')
new_task_parser.add_argument('listid', type=int, help='ID of LIST to add new TASK to.')
new_task_parser.add_argument('title', type=str, help='Title of the new TASK.')
new_task_parser.add_argument('-d','--desc', type=str, help='Description for TASK.', default='No Description Available.')
new_task_parser.add_argument('-p', '--prior', type=str, help='Add a priority for TASK.', choices=['HIGH', 'LOW', 'MED', 'EMERGENCY'], default='MED')
new_task_parser.add_argument('-s', '--status', type=str, help='Status of TASK', default='Incomplete')

# new todolist
new_list_parser = command_parser.add_parser('new-list', help='Create a new LIST.')
new_list_parser.add_argument('title', type=str, help='Name of new LIST.')
new_list_parser.add_argument('-d','--desc', type=str, help='Description for LIST.', default='No Description Available.')
new_list_parser.add_argument('-s', '--status', type=str, help='Status of LIST', default='Incomplete')

# remove/shift task
remove_task_parser = command_parser.add_parser('remove-task', help='Remove a TASK from a LIST.')
remove_task_parser.add_argument('listid', type=int, help='ID of LIST to remove TASK from.')
remove_task_parser.add_argument('id', type=int, help='ID of TASK to be removed in context of specified LIST. (default: 1)', default=1)
remove_task_parser.add_argument('-s', '--shift-to', type=int, help='ID of LIST for TASK to be shifted to.')

# remove list
remove_list_parser = command_parser.add_parser('remove-list', help='Delete a LIST from current working dir.')
remove_list_parser.add_argument('listid', type=int, help='ID of LIST to be deleted.')

# mark task with a status
status_task_parser = command_parser.add_parser('mark-task', help='Mark a TASK with a status.')
status_task_parser.add_argument('listid', type=int, help='ID of LIST to mark status of TASK from.')
status_task_parser.add_argument('id', type=int, help='ID of TASK to mark status of. (default: 1)', default=1)
status_task_parser.add_argument('status', type=str, help='Status for TASK, a length of one word is recommended. (default: Complete)', default='Complete')

# mark list with a status
status_list_parser = command_parser.add_parser('mark-list', help='Mark a LIST with a status.')
status_list_parser.add_argument('listid', type=int, help='ID of LIST to mark status of.')
status_list_parser.add_argument('status', type=str, help='Status for LIST, a length of one word is recommended. (default: Complete)', default='Complete')

# edit task
edit_task_parser = command_parser.add_parser('edit-task', help='Edit a TASK in a LIST.')
edit_task_parser.add_argument('listid', type=int, help='ID of LIST containing TASK to be edited.')
edit_task_parser.add_argument('id', type=int, help='ID of TASK to be edited. (default: 1)', default=1)
edit_task_parser.add_argument('-t','--title', type=str, help='Edit title for TASK.', default=None)
edit_task_parser.add_argument('-d','--desc', type=str, help='Edit description for TASK.', default=None)
edit_task_parser.add_argument('-p', '--prior', type=str, help='Edit priority for TASK.', choices=['HIGH', 'LOW', 'MED', 'EMERGENCY'], default=None)
edit_task_parser.add_argument('-s', '--status', type=str, help='Edit status of TASK', default=None)

# edit list
edit_list_parser = command_parser.add_parser('edit-list', help='Edit a LIST.')
edit_list_parser.add_argument('listid', type=int, help='ID of LIST to be edited.')
edit_list_parser.add_argument('-t','--title', type=str, help='Edit title for LIST.', default=None)
edit_list_parser.add_argument('-d','--desc', type=str, help='Edit description for LIST.', default=None)
edit_list_parser.add_argument('-s', '--status', type=str, help='Edit status of LIST', default=None)

# Search tasks
search_task_parser = command_parser.add_parser('search-tasks', help='Search for TASKs based on various criteria.')
search_task_parser.add_argument('-t','--title', type=str, help='Search for TASKs with a specific name (case-insensitive).', default=None)
search_task_parser.add_argument('-d', '--desc', type=str, help='Search for TASKs with a specific description (case-insensitive).', default=None)
search_task_parser.add_argument('-p', '--prior', type=str, help='Search for TASKs with a specific priority.', choices=['HIGH', 'LOW', 'MED', 'EMERGENCY'], default=None)
search_task_parser.add_argument('-s', '--status', type=str, help='Search for TASKs with a specific status.', default=None)

# Search lists
search_list_parser = command_parser.add_parser('search-lists', help='Search for LISTs based on various criteria.')
search_list_parser.add_argument('-t', '--title', type=str, help='Search for LISTs with a specific name (case-insensitive).', default=None)
search_list_parser.add_argument('-d','--desc', type=str, help='Search for LISTs with a specific description (case-insensitive).', default=None)
search_list_parser.add_argument('-s','--status', type=str, help='Search for LISTs with a specific status.', default=None)
search_list_parser.add_argument('-n','--number-of-tasks', type=int, help='Search for LISTs with task number above this value.', default=None)


# ========= UTIL ================= #

def init_todo_db(filedir='todo.db'):
    if not path.exists(filedir):
        write_db({'lists':[], 'config': {}})

def get_db(filedir='todo.db'):
    with open(filedir, 'r') as file:
        data = json.load(file)
    return data

def write_db(data, filedir='todo.db'):
    with open(filedir, 'w') as file:
        json.dump(data, file)

def update_db(data, filedir='todo.db'):
    data_ = get_db()
    data_.update(data)
    write_db(data_)

# ========== HANDLERS ============ #

def get_tasks(args):
    data = get_db()
    if args.listid <= 0 or args.listid > len(data['lists']):
        print("LIST ID cannot be 0 or less or greater than existing amount of LISTs.")
    else:
        list_ = data['lists'][args.listid-1]
        print(f'Tasks in list "{list_['name']}" (ID: {args.listid}):\n')
        for i, task in enumerate(list_['tasks']):
            print(f'{i+1}. {task['name']}\n  DESCRIPTION: {task['desc']}\n  STATUS: {task['status']}\n  PRIORITY: {task['prior']}')

def get_lists(args):
    data = get_db()
    print('Available Lists:\n')
    for i, list_ in enumerate(data['lists']):
        print(f'{i+1}. {list_['name']} - "{list_['desc']}"\n   STATUS: {list_['status']}\n   NUMBER OF TASKS: {len(list_['tasks'])}\n')

def new_task(args):
    data = get_db()
    if args.listid <= 0 or args.listid > len(data['lists']):
        print("LIST ID cannot be 0 or less or greater than existing amount of LISTs.")
    else:
        data['lists'][args.listid-1]['tasks'].append({
            'name': args.title,
            'desc': args.desc,
            'prior': args.prior,
            'status': args.status,
        })
        update_db(data)
        print(f'TASK ID {len(data['lists'][args.listid-1]['tasks'])} "{args.title}" was added to LIST ID {args.listid} "{data['lists'][args.listid-1]['name']}".')


def new_list(args):
    data = get_db()
    data['lists'].append({
        'name': args.title,
        'desc': args.desc,
        'status': args.status,
        'tasks': []
    })
    print(f'')
    update_db(data)
    print(f'LIST ID {len(data['lists'])} "{args.title}" Created.')

def remove_task(args):
    data = get_db()
    if args.listid <= 0 or args.listid > len(data['lists']):
        print("LIST ID cannot be 0 or less or greater than existing amount of LISTs.")
    else:
        list_ = data['lists'][args.listid - 1]
        if args.id <= 0 or args.id > len(list_['tasks']):
            print(f"TASK ID cannot be 0 or less or greater than the number of tasks in the list '{list_['name']}' (ID: {args.listid}).")
        else:
            removed_task = list_['tasks'].pop(args.id - 1)
            if args.shift_to:
                if 0 < args.shift_to < len(data['lists']):
                    data['lists'][args.shift_to-1]['tasks'].append(removed_task)
                    print(f'Shifted TASK to LIST ID {args.shift_to}.\n')
                else:
                    print("LIST ID to shift to cannot be out of range.")
            update_db(data)
            print(f'TASK ID {args.id} "{removed_task['name']}" was removed from LIST ID {args.listid} "{list_['name']}".')

def remove_list(args):
    data = get_db()
    if args.listid <= 0 or args.listid > len(data['lists']):
        print("LIST ID cannot be 0 or less or greater than existing amount of LISTs.")
    else:
        removed_list = data['lists'].pop(args.listid - 1)
        update_db(data)
        print(f'LIST ID {args.listid} "{removed_list['name']}" was removed.')

def mark_task(args):
    data = get_db()
    if args.listid <= 0 or args.listid > len(data['lists']):
        print("LIST ID cannot be 0 or less or greater than existing amount of LISTs.")
    else:
        list_ = data['lists'][args.listid - 1]
        if args.id <= 0 or args.id > len(list_['tasks']):
            print(f"TASK ID cannot be 0 or less or greater than the number of tasks in the list '{list_['name']}' (ID: {args.listid}).")
        else:
            list_['tasks'][args.id - 1]['status'] = args.status
            update_db(data)
            print(f'TASK ID {args.id} in LIST ID {args.listid} was marked as "{args.status}".')

def mark_list(args):
    data = get_db()
    if args.listid <= 0 or args.listid > len(data['lists']):
        print("LIST ID cannot be 0 or less or greater than existing amount of LISTs.")
    else:
        data['lists'][args.listid - 1]['status'] = args.status
        update_db(data)
        print(f'LIST ID {args.listid} was marked as "{args.status}".')

def edit_task(args):
    data = get_db()
    if args.listid <= 0 or args.listid > len(data['lists']):
        print("LIST ID cannot be 0 or less or greater than existing amount of LISTs.")
    else:
        list_ = data['lists'][args.listid - 1]
        if args.id <= 0 or args.id > len(list_['tasks']):
            print(f"TASK ID cannot be 0 or less or greater than the number of tasks in the list '{list_['name']}' (ID: {args.listid}).")
        else:
            task = list_['tasks'][args.id - 1]
            if args.title is not None:
                task['name'] = args.title
            if args.desc is not None:
                task['desc'] = args.desc
            if args.prior is not None:
                task['prior'] = args.prior
            if args.status is not None:
                task['status'] = args.status
            update_db(data)
            print(f'TASK ID {args.id} in LIST ID {args.listid} was edited.')

def edit_list(args):
    data = get_db()
    if args.listid <= 0 or args.listid > len(data['lists']):
        print("LIST ID cannot be 0 or less or greater than existing amount of LISTs.")
    else:
        list_ = data['lists'][args.listid - 1]
        if args.title is not None:
            list_['name'] = args.title
        if args.desc is not None:
            list_['desc'] = args.desc
        if args.status is not None:
            list_['status'] = args.status
        update_db(data)
        print(f'LIST ID {args.listid} was edited.')

def search_tasks(args):
    data = get_db()
    
    search_results = []
    
    # Iterate through all lists and their tasks
    for list_id, to_do_list in enumerate(data['lists'], start=1):
        for task_id, task in enumerate(to_do_list['tasks'], start=1):
            # Check if the task matches the search criteria
            if (
                (not args.title or args.title.lower() in task['name'].lower()) and
                (not args.desc or args.desc.lower() in task.get('desc', '').lower()) and
                (not args.prior or args.prior == task.get('prior')) and
                (not args.status or args.status == task.get('status'))
            ):
                search_results.append({
                    'list_id': list_id,
                    'list_name': to_do_list['name'],
                    'task_id': task_id,
                    'task_name': task['name'],
                    'task_desc': task.get('desc', 'No Description Available'),
                    'task_prior': task.get('prior', 'Not Set'),
                    'task_status': task.get('status', 'Incomplete')
                })
    
    if search_results:
        print("Search Results:\n")
        for i, result in enumerate(search_results, start=1):
            print(f"{i}. List ID: {result['list_id']}, List Name: '{result['list_name']}'")
            print(f"  Task ID: {result['task_id']}, Task Name: '{result['task_name']}'")
            print(f"  Task Description: '{result['task_desc']}'")
            print(f"  Task Priority: {result['task_prior']}")
            print(f"  Task Status: {result['task_status']}\n")
    else:
        print("No tasks matching the search criteria were found.")

def search_lists(args):
    data = get_db()

    search_results = []

    for list_id, to_do_list in enumerate(data['lists'], start=1):
        if (
            (not args.title or args.title.lower() in to_do_list['name'].lower()) and
            (not args.desc or args.desc.lower() in to_do_list.get('desc', '').lower()) and
            (not args.status or args.status == to_do_list.get('status')) and
            (not args.number_of_tasks or args.number_of_tasks <= len(to_do_list.get('tasks', [])))
        ):
            search_results.append({
                'list_id': list_id,
                'list_name': to_do_list['name'],
                'list_desc': to_do_list.get('desc', 'No Description Available'),
                'list_status': to_do_list.get('status', 'Incomplete'),
                'num_tasks': len(to_do_list['tasks'])
            })

    if search_results:
        print("Search Results:\n")
        for i, result in enumerate(search_results, start=1):
            print(f"{i}. List ID: {result['list_id']}, List Name: '{result['list_name']}'")
            print(f"  List Description: '{result['list_desc']}'")
            print(f"  List Status: {result['list_status']}")
            print(f"  Number of Tasks: {result['num_tasks']}\n")
    else:
        print("No lists matching the search criteria were found.")

command_lookup = {
    'get-tasks': get_tasks,
    'get-lists': get_lists,
    'new-task': new_task,
    'new-list': new_list,
    'remove-task': remove_task,
    'remove-list': remove_list,
    'mark-task': mark_task,
    'mark-list': mark_list,
    'edit-task': edit_task,
    'edit-list': edit_list,
    'search-tasks': search_tasks,
    'search-lists': search_lists,
}
# ================================ #

# Initialize
init_todo_db()
args = parser.parse_args()

print()
if args.command:
    callback = command_lookup.get(args.command, None)
    if callback:
        try:
            callback(args)
        except KeyError:
            print('An issue was detected with todo.db, please correct or delete and reinitialize.')
    else:
        print('This command currently does not have a handler.')
else:
    print('No commands supplied. Try "todo.py --help".')
print()