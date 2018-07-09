from peewee import *
from collections import OrderedDict
import datetime
import os
import sys

db = SqliteDatabase('work-log.db')


class Task(Model):
    employee_name = CharField(max_length=255)
    time_worked = IntegerField()
    task_name = CharField(max_length=255)
    general_notes = CharField(max_length=255, default="None")
    timestamp = DateField(default=datetime.date.today())

    class Meta:
        database = db


def initialize():
    db.connect()
    db.create_tables([Task], safe=True)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def add_entry():
    """Add an entry."""
    name = input('enter Employee name: ').strip()
    time = int(input('time spent on task in minutes : ').strip())
    task = input('enter task name: ').strip()
    notes = input('if you have additional notes write now else type n').strip()

    if name and time and task:
        if notes.lower() == 'n':
            if input('enter y to save entry: ').lower() == 'y':
                Task.create(employee_name=name,
                            time_worked=time,
                            task_name=task,
                            )
                print("Saved successfully!")
        else:
            if input('enter y to save entry: ').lower() == 'y':
                Task.create(employee_name=name,
                            time_worked=time,
                            task_name=task,
                            general_notes=notes
                            )
                print("Saved successfully!")


def view_entries(search_task=None,
                 employee_find=None,
                 date_find=None,
                 time_find=None):
    """View all previous entries."""
    entries = Task.select().order_by(Task.timestamp.desc())
    if search_task:
        entries = entries.where(Task.general_notes.contains(search_task) |
                                Task.task_name.contains(search_task))
    elif employee_find:
        entries = entries.where(Task.employee_name == employee_find)
    elif date_find:
        entries = entries.where(Task.timestamp == datetime.datetime.strptime(
            date_find, '%d/%m/%Y'))
    elif time_find:
        entries = entries.where(Task.time_worked == int(time_find))

    for entry in entries:
        timestamp = entry.timestamp.strftime('%d/%m/%Y')
        clear()
        print(timestamp)
        print('=' * len(timestamp))
        print('Empolyee: ' + entry.employee_name)
        print('Task name: ' + entry.task_name)
        print('Time worked: ' + str(entry.time_worked) + ' minutes')
        print('Notes: ' + entry.general_notes)
        print('\n\n' + '=' * len(timestamp))
        print('n) next entry')
        print('d) delete entry')
        print('q) return to main menu')

        next_action = input('Action: [Ndq] ').lower().strip()
        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_entry(entry)



def menu_loop():
    """Show the menu"""
    choice = None

    while choice != 'q':
        clear()
        print("Enter 'q' to quit.")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()

        if choice in menu:
            clear()
            menu[choice]()


def delete_entry(entry):
    """Delete an entry."""
    if input("enter y to confirm").lower() == 'y':
        entry.delete_instance()
        print("Entry deleted!")


def look_up_preivous_entries():
    """Search for previous entries"""
    choice = None

    while choice != 'b':
        clear()
        print("Enter 'b' to go back.")
        for key, value in search_menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()

        if choice in search_menu:
            clear()
            search_menu[choice]()


def search_by_employee():
    """Search by employee."""
    view_entries(None, input('Search query: '), None, None)


def search_by_time():
    """Search by time spent on task (minutes)."""
    try:
        view_entries(None, None, None, input('Search query: '))
    except ValueError:
        print('please enter numbers only')



def search_by_date():
    """Search by a date of task(dd/mm/yyyy)"""
    try:
        view_entries(None, None, input('Search query: '), None)
    except ValueError:
        print('Please enter a date in dd/mm/yyyy format')

def search_by_task_or_notes():
    """Search by task name or notes."""
    view_entries(input('Search query: '), None, None, None)


search_menu = OrderedDict([
    ('e', search_by_employee),
    ('t', search_by_time),
    ('d', search_by_date),
    ('n', search_by_task_or_notes)
])

menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
    ('s', look_up_preivous_entries),
])


if __name__ == '__main__':
    initialize()
    menu_loop()
