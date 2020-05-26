# Add a book to the library
# Delete a book from the library
# Lend a book
# Get a book returned
# Print list of books, and the return date if lent out

# Write functions that do the things you want, call those functions from you CLI functions
# Look out for squiggly lines
# Convert to JSON with a dictionary
# Key is the book title value is another dictionary, keys=[title, author, lent_date]
import click
import json
# import datetime

# Creating dictionary and assigning it to variable called file
with open('personal_library.json') as f:
    file = json.load(f)


def check_book_in_library(book_name):
    """Checks if the book is in the library without case sensitivity"""
    book_name = book_name.lower().strip()
    for key in file.keys():
        if book_name == key.lower().strip():
            return True
    return False


def add_book_to_library(book_name):
    """Takes book_name and puts it as a new key and title value on the file dictionary"""
    book_name = book_name.title()
    file[book_name] = {"title": book_name, "return_date": None}
    with open('personal_library.json', 'w') as f:
        json.dump(file, f)


def delete_book_from_library(book_name):
    """Takes book_name and deletes the key that matches it, and its values with it"""
    book_name = book_name.title()
    file.pop(book_name)
    with open('personal_library.json', 'w') as f:
        json.dump(file, f)


def lend_book_from_library(book_name):
    """Searches for book_name within the keys of the dict, then adds a return_date as one of the values"""
    book_name = book_name.title()
    date_string = input("Date of return yyyy-mm-dd: ")
    # date_object = datetime.datetime.strptime(date_string, "%Y/%m/%d") not using this for now
    file[book_name]["return_date"] = date_string
    with open('personal_library.json', 'w') as f:
        json.dump(file, f)
    return date_string


def return_book_to_library(book_name):
    """Searches for the key with the name book_name, then changes the return_date value to None"""
    book_name = book_name.title()
    file[book_name]["return_date"] = None
    with open('personal_library.json', 'w') as f:
        json.dump(file, f)


def check_if_lent(book_name):
    """Searches for the key with the name of book_name, then checks if the return_date value is None
    returns true if the value is different than None"""
    book_name = book_name.title()
    return file[book_name]["return_date"] is not None


def print_all_books():
    """Prints the entire list of title values in the dict"""
    for book in file:
        lent = (file[book]["return_date"])
        # Also works with the primery key instead of the title key, but in case I decide
        # to change the keys on the json file, the title key will always return the title
        print(f'{file[book]["title"]} \t\t {"" if lent is None else lent}')


@click.group()
def cli():
    pass


@click.command()
@click.option("--name", prompt="Book Name", help="Name of the book to add")
def add_book(name):
    """Add a book to your library. Answer the prompt with the name of the book"""
    if check_book_in_library(name):
        msg = f"{name} is already in the Library"
    else:
        add_book_to_library(name)
        msg = f"{name} added to the Library"
    click.echo(msg)


@click.command()
@click.option("--name", prompt="Book Name, enter to cancel", default="", help="Name of the book to delete")
def delete_book(name):
    """Remove a book from your library. Answer the prompt with the name of the book"""
    if check_book_in_library(name):
        delete_book_from_library(name)
        msg = f"Deleted {name} from the library"
    else:
        msg = ("" if name == "" else f"{name} was not found in the Library")
    click.echo(msg)


@click.command()
@click.option("--name", prompt="Book Name, enter to cancel", default="", help="Name of the book to lend")
def lend_book(name):
    """Lend a book from your library. Answer the prompt with the name of the book and date of return"""
    if check_book_in_library(name):
        if check_if_lent(name):
            msg = f"{name} is already lent, wait for it to get returned"
        else:
            date = lend_book_from_library(name)
            msg = f"{name} lent until {date}"
    else:
        msg = f"{name} is not in the Library"
    click.echo(msg)


@click.command()
@click.option("--name", prompt="Book Name", help="Name of the book to return")
def return_book(name):
    """Return a book to your library. Answer the prompt with the name of the book"""
    if check_book_in_library(name):
        if check_if_lent(name):
            return_book_to_library(name)
            msg = f"{name} returned to the Library"
        else:
            msg = f"{name} does not need to be returned"
    else:
        msg = f"{name} is not part of the Library"
    click.echo(msg)


@click.command()
def print_book_list():
    """Prints the entire list of books. With return dates for books lent"""
    print_all_books()


cli.add_command(add_book)
cli.add_command(delete_book)
cli.add_command(lend_book)
cli.add_command(return_book)
cli.add_command(print_book_list)

if __name__ == '__main__':
    cli()


# Create a function to avoid certain names to be written such as an empty space or a dot
# Create function that really checks without case sensitivity, currently 3G != 3g when it should be the same
