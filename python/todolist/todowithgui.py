import argparse
import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, Label, Entry, Listbox, Button, END, Text
from os import path



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

PRIORITY_COLORS = {
    "LOW": "blue",
    "MED": "green",
    "HIGH": "orange",
    "EMERGENCY": "red",
}

# Initialize the Tkinter GUI
class TodoGUI:
    def __init__(self, root):
        self.root = root
        root.title("TODO")
        self.task_frame = tk.Frame(root, padx=10, relief="groove", borderwidth=2, pady=12)
        self.task_info_frame = tk.Frame(root, padx=10, relief="groove", borderwidth=2)
        self.title_label = Label(self.task_frame, text="Choose list:")
        self.title_label.pack(anchor="w")
        self.lists_combobox = ttk.Combobox(self.task_frame, state="readonly", width=60)
        self.lists_combobox.pack()
        self.lists_combobox.bind("<<ComboboxSelected>>", self.on_list_selected)
        self.tasks_label = Label(self.task_frame, text="Tasks in list:")
        self.tasks_label.pack(anchor="w")

        self.tasks_listbox = Listbox(self.task_frame, selectmode=tk.SINGLE, width=60)
        self.tasks_listbox.pack()
        self.tasks_listbox.bind("<<ListboxSelect>>", self.on_task_selected)

        self.task_frame.pack(side="left")

        self.switch_info_var = tk.StringVar(value="Task Info")

        self.info_switch = tk.OptionMenu(self.task_info_frame, self.switch_info_var, "Task Info", "List Info", command=self.switch_info)
        self.info_switch.pack(anchor="w")


        self.task_info_frame.pack(side="left")

        # Task information labels and entry fields
        self.field_labels = {}
        self.field_entries = {}
        self.task_data = {
            "task_name": tk.StringVar(),
            "task_desc": tk.StringVar(),
            "task_prior": tk.StringVar(),
            "task_status": tk.StringVar(),
        }

        # List information labels and entry fields
        self.list_field_labels = {}
        self.list_field_entries = {}
        self.list_data = {
            "list_name": tk.StringVar(),
            "list_desc": tk.StringVar(),
            "list_status": tk.StringVar(),
            "num_tasks": tk.StringVar(),
        }

        self.subtask_info_frame = tk.Frame(self.task_info_frame, padx=10, pady=10)

        self.create_field("Name", "task_name", self.task_data, self.subtask_info_frame)
        self.create_field("Description", "task_desc", self.task_data, self.subtask_info_frame)
        self.create_priority_buttons(self.subtask_info_frame)
        self.create_field("Status", "task_status", self.task_data, self.subtask_info_frame)

        self.list_info_frame = tk.Frame(self.task_info_frame, padx=10, pady=50)
        # Create list information fields
        self.create_field("List Name", "list_name", self.list_data, self.list_info_frame)
        self.create_field("List Description", "list_desc", self.list_data, self.list_info_frame)
        self.create_field("List Status", "list_status", self.list_data, self.list_info_frame)
        self.create_field("Number of Tasks", "num_tasks", self.list_data, self.list_info_frame)

        self.list_info_frame.pack(side="left")
        self.list_info_frame.pack_forget()

        self.task_entry_frame = tk.Frame(self.task_frame)
        self.input_label = Label(self.task_entry_frame, text="Input: ")
        self.input_label.pack(anchor="w")
        self.task_entry = Entry(self.task_entry_frame, width=60)
        self.task_entry.pack()

        self.add_task_button = Button(self.task_entry_frame, text="Add Task", command=self.add_task)
        self.add_task_button.pack(side="left", padx=5, pady=5)

        self.add_list_button = Button(self.task_entry_frame, text="Add List", command=self.add_list)
        self.add_list_button.pack(side='left', padx=5, pady=5)

        self.remove_task_button = Button(self.task_entry_frame, text="Remove Task", command=self.remove_task)
        self.remove_task_button.pack(side="left", padx=5, pady=5)

        self.remove_list_button = Button(self.task_entry_frame, text="Remove List", command=self.remove_list)
        self.remove_list_button.pack(side="left", padx=5, pady=5)

        self.mark_task_button = Button(self.task_entry_frame, text="Mark Task", command=self.mark_task)
        self.mark_task_button.pack(side="left", padx=5, pady=5)

        self.update_button = Button(self.task_info_frame, text="Update", command=self.update_info)
        self.update_button.pack(anchor="s", padx=5, pady=5)

        self.task_entry_frame.pack(side="bottom")

        self.list_lists()
        self.switch_info()

    def switch_info(self, wth=None):
        info_type = self.switch_info_var.get()
        if info_type == "Task Info":
            self.show_task_info()
            self.subtask_info_frame.pack(side="left")
            self.list_info_frame.pack_forget()  # Hide the list information frame
        elif info_type == "List Info":
            self.show_list_info()
            self.subtask_info_frame.pack_forget()  # Hide the task information frame
            self.list_info_frame.pack(side="left")

    def create_field(self, label_text, field_name, data_dict, frame):
        label = Label(frame, text=label_text)
        label.pack(anchor="w")
        entry = Entry(frame, textvariable=data_dict[field_name], width=40)
        entry.pack(anchor="w")
        self.field_labels[field_name] = label
        self.field_entries[field_name] = entry

    # ...

    def show_list_info(self):
        selected_list_index = self.get_selected_list_index()
        if selected_list_index is not None:
            data = get_db()
            selected_list = data["lists"][selected_list_index]
            self.list_data["list_name"].set(selected_list["name"])
            self.list_data["list_desc"].set(selected_list.get("desc", ""))
            self.list_data["list_status"].set(selected_list.get("status", "Incomplete"))
            num_tasks = len(selected_list["tasks"])
            self.list_data["num_tasks"].set(num_tasks)

    def create_priority_buttons(self, frame):
        label = Label(frame, text="Priority")
        label.pack(anchor="w")
        priorities = ["LOW", "MED", "HIGH", "EMERGENCY"]
        for priority in priorities:
            tk.Radiobutton(
                frame,
                text=priority,
                variable=self.task_data["task_prior"],
                value=priority,
            ).pack(anchor="w")

    def on_list_selected(self, event):
        self.list_tasks()  # Update the task list when a list is selected
        self.show_list_info()

    def on_task_selected(self, event):
        self.show_task_info()  # Show task info when a task is selected

    def show_task_info(self):
        selected_list_index = self.get_selected_list_index()
        selected_task_index = self.get_selected_task_index()
        if selected_list_index is not None and selected_task_index is not None:
            data = get_db()
            selected_list = data["lists"][selected_list_index]
            selected_task = selected_list["tasks"][selected_task_index]
            self.task_entry.delete(0, END)
            self.task_entry.insert(0, selected_task["name"])
            self.task_data["task_name"].set(selected_task["name"])
            self.task_data["task_desc"].set(selected_task.get("desc", ""))
            self.task_data["task_prior"].set(selected_task.get("prior", "MED"))
            self.task_data["task_status"].set(selected_task.get("status", "Incomplete"))

    def update_info(self):
        selected_list_index = self.get_selected_list_index()
        selected_task_index = self.get_selected_task_index()
        if selected_list_index is not None and selected_task_index is not None:
            data = get_db()
            selected_list = data["lists"][selected_list_index]
            selected_task = selected_list["tasks"][selected_task_index]

            selected_task["name"] = self.task_data["task_name"].get()
            selected_task["desc"] = self.task_data["task_desc"].get()
            selected_task["prior"] = self.task_data["task_prior"].get()
            selected_task["status"] = self.task_data["task_status"].get()

            selected_list["name"] = self.list_data["list_name"].get()
            selected_list["desc"] = self.list_data["list_desc"].get()
            selected_list["status"] = self.list_data["list_status"].get()

            update_db(data)
            self.list_tasks()

            if self.switch_info_var.get() == "List Info":
                self.list_lists()

    def list_lists(self):
        self.lists_combobox.set("")
        data = get_db()
        list_names = [list_["name"] for list_ in data["lists"]]
        self.lists_combobox["values"] = list_names

    def list_tasks(self):
        self.tasks_listbox.delete(0, tk.END)
        selected_list_index = self.get_selected_list_index()
        if selected_list_index is not None:
            data = get_db()
            selected_list = data["lists"][selected_list_index]

            self.tasks_listbox.bind("<<ListboxSelect>>", self.update_selected_task_color)

            for i, task in enumerate(selected_list["tasks"]):
                task_display = f"{i + 1}. {task['name']} [{task['status']}]"
                self.tasks_listbox.insert(tk.END, task_display)
                # Change background color based on priority
                priority_color = PRIORITY_COLORS.get(task.get("prior", "MED"), "white")
                self.tasks_listbox.itemconfig(i, {'bg': priority_color})

            # Show the task information for the first task in the list
            if selected_list["tasks"]:
                self.tasks_listbox.selection_set(0)
                self.show_task_info()

    def update_selected_task_color(self, event):
        selected_task_index = self.get_selected_task_index()
        self.show_task_info()
        if selected_task_index is not None:
            data = get_db()
            selected_list_index = self.get_selected_list_index()
            selected_list = data["lists"][selected_list_index]
            selected_task = selected_list["tasks"][selected_task_index]
            # Change background color based on priority
            priority_color = PRIORITY_COLORS.get(selected_task.get("prior", "MED"), "white")
            
            self.tasks_listbox.configure(selectbackground="dark"+priority_color)
            


    def add_task(self):
        selected_list_index = self.get_selected_list_index()
        if selected_list_index is not None:
            data = get_db()
            selected_list = data['lists'][selected_list_index]
            task_name = self.task_entry.get()
            if task_name:
                selected_list['tasks'].append({
                    'name': task_name,
                    'desc': 'No Description Available',
                    'prior': 'MED',
                    'status': 'Incomplete'
                })
                self.task_entry.delete(0, END)
                update_db(data)
                self.list_tasks()

    def add_list(self):
        list_name = self.task_entry.get()
        if list_name:
            data = get_db()
            data['lists'].append({
                'name': list_name,
                'desc': 'No Description Available',
                'status': 'Incomplete',
                'tasks': []
            })
            self.lists_combobox.set('')
            update_db(data)
            self.list_lists()
        self.task_entry.delete(0, END)

    def remove_task(self):
        selected_list_index = self.get_selected_list_index()
        selected_task_index = self.get_selected_task_index()
        if selected_list_index is not None and selected_task_index is not None:
            data = get_db()
            selected_list = data['lists'][selected_list_index]
            removed_task = selected_list['tasks'].pop(selected_task_index)
            update_db(data)
            self.list_tasks()

    def remove_list(self):
        selected_list_index = self.get_selected_list_index()
        if selected_list_index is not None:
            data = get_db()
            data['lists'].pop(selected_list_index)
            update_db(data)
            self.list_lists()

    def mark_task(self):
        selected_list_index = self.get_selected_list_index()
        selected_task_index = self.get_selected_task_index()
        if selected_list_index is not None and selected_task_index is not None:
            data = get_db()
            selected_list = data['lists'][selected_list_index]
            selected_task = selected_list['tasks'][selected_task_index]
            selected_task['status'] = 'Complete' if selected_task['status'] == 'Incomplete' else 'Incomplete'
            update_db(data)
            self.list_tasks()

    def get_selected_list_index(self):
        selected = self.lists_combobox.get()
        data = get_db()
        list_names = [list_['name'] for list_ in data['lists']]
        if selected in list_names:
            return list_names.index(selected)
        return None

    def get_selected_task_index(self):
        selected = self.tasks_listbox.curselection()
        if selected:
            return int(selected[0])
        return None

def main():
    parser = argparse.ArgumentParser(prog='todo.py', description="Command line application for efficient management of tasks to be done.", epilog='END')
    command_parser = parser.add_subparsers(dest='command', help='Available commands', title='Commands')

    gui_parser = command_parser.add_parser('gui', help="Launch GUI for Command Line Application.")

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

    # Define your command line commands as you did before
    init_todo_db()
    args = parser.parse_args()

    if args.command == 'gui':
        root = tk.Tk()
        app = TodoGUI(root)
        root.mainloop()
    elif args.command:
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

if __name__ == "__main__":
    main()
