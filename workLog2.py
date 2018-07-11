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


def add_entry(name,
              time,
              task,
              notes):
    """Add an entry."""
    name.strip()
    time = int(time.strip())
    task.strip()
    notes.strip()
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


def view_entries():
    """View all previous entries."""
    return Task.select().order_by(Task.timestamp.desc())


def view_entries_loop(entries):
    '''View all previous entries.'''
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
            if choice.lower() == 'a':
                clear()
                try:
                    menu[choice](input('name'),
                                 input('time'),
                                 input('task'),
                                 input('notes'))
                except ValueError:
                    print('Please enter numbers for time ')
            elif choice.lower() == 'v':
                clear()
                menu[choice](view_entries())
            elif choice.lower() == 's':
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
            if choice == 'e':
                clear()
                view_entries_loop(search_menu[choice]
                                  (input('enter employee name :')))
            elif choice == 't':
                clear()
                try:
                    view_entries_loop(search_menu[choice]
                                      (input('enter time spent (minutes) :')))
                except ValueError:
                    print('please enter numbers only ')

            elif choice == 'd':
                clear()
                try:
                    view_entries_loop(search_menu[choice]
                                      (input('enter date of '
                                             'task (dd/mm/yyyy) :')))
                except ValueError:
                    print('please enter dd/mm/yyyy format')

            elif choice == 'n':
                clear()
                view_entries_loop(search_menu[choice]
                                  (input('enter word within task name or '
                                         'notes :')))


def search_by_employee(employee_find):
    """Search by employee."""
    return view_entries().where(Task.employee_name == employee_find)


def search_by_time(time_find):
    """Search by time spent on task (minutes)."""
    return view_entries().where(Task.time_worked == int(time_find))


def search_by_date(date_find):
    """Search by a date of task(dd/mm/yyyy)"""
    return view_entries().where(Task.timestamp == datetime.datetime.strptime(
        date_find, '%d/%m/%Y'))


def search_by_task_or_notes(search_task):
    """Search by task name or notes."""
    return view_entries().where(Task.general_notes.contains(search_task) |
                                Task.task_name.contains(search_task))


search_menu = OrderedDict([
    ('e', search_by_employee),
    ('t', search_by_time),
    ('d', search_by_date),
    ('n', search_by_task_or_notes)
])

menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries_loop),
    ('s', look_up_preivous_entries),
])

if __name__ == '__main__':
    initialize()
    menu_loop()
