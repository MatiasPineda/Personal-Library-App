# Add a book to the library
# Delete a book from the library
# Lend a book
# Get a book returned
# Print list of books, and the return date if lent out

# Write functions that do the things you want, call those functions from you CLI functions
# Look out for squiggly lines
# Convert to JSON with a dictionary
# Key is the book title value is another dictionary, keys=[title, author, lent_date]
library = {
    "Can't Hurt Me": {
        "title": "Can't Hurt Me",
        "author": "David Goggins",
        "return_date": "2020-05-12",  # or None. Check out date.strptime and strftime
    }
}


import click


@click.group()
def cli():
    pass

@click.command()
@click.option("--name", prompt="Book Name", help="Name of the book to add")
def add_book(name):
    """Add a book to your library. Answer the prompt with the name of the book"""
    book_name = f"{name}\n"  # Convert two word variables to snake case
    # Leave the book_name without the \n and add it as needed
    # Use a context to open and close files
    with open("personal_library.txt", "r") as file:
        pass  # code goes in here

    file = open("personal_library.txt", "r")
    for _ in file.readlines():  # give this variable a name
        # line = 'Apple\n'
        # name = 'Orange and Apple\n'
        if book_name in _:
            click.echo("%s is already in the Library" %name)  # Convert to f-strings
            file.close()
            return
    file.close()
    file = open("personal_library.txt", "a")
    file.write(book_name)
    file.close()
    click.echo("%s added to the library" %name)

@click.command()
@click.option("--name", prompt="Book Name, enter to cancel", default="", help="Name of the book to delete")
def delete_book(name):
    """Remove a book from your library. Answer the prompt with the name of the book"""
    bookname = f"{name}\n"
    file = open("personal_library.txt", "r")
    booklist = file.readlines()
    file.close()
    if name == "":
        return
    elif bookname in booklist:
        booklist.remove(bookname)
        file=open("personal_library.txt", "w")
        file.write("".join(booklist))
        click.echo("Deleted %s from the library" %name)
        file.close()
    else:
        click.echo("%s not found, try print-booklist command to see available books" %name)

@click.command()
@click.option("--name", prompt="Book Name, enter to cancel", default="", help="Name of the book to lend")
def lend_book(name):
    """Lend a book from your library. Answer the prompt with the name of the book and date of return"""
    bookname = f"{name}\n"
    file = open("personal_library.txt", "r")
    booklist = file.readlines()
    file.close()
    if name == "":
        return
    elif bookname in booklist:
        return_date = input("Return Date: ")
        booklist[booklist.index(bookname)] = f"{name} \t lent until {return_date}\n"
        file = open("personal_library.txt", "w")
        file.write("".join(booklist))
        click.echo("%s lent until %s" %(name, return_date))
        file.close()
    else:
        click.echo("%s not found or already lent, try print-booklist command to see available books" % name)

@click.command()
@click.option("--name", prompt="Book Name", help="Name of the book to return")
def return_book(name):
    """Return a book to your library. Answer the prompt with the name of the book"""
    bookname = f"{name}\n"
    file = open("personal_library.txt", "r")
    booklist = file.readlines()
    file.close()
    if name == "":
        return
    else:
        for _ in booklist:
            if name in _:
                if bookname == _:
                    click.echo("%s does not need to be returned" % name)
                    file.close()
                    return
                booklist[booklist.index(_)] = f"{name}\n"
                file = open("personal_library.txt", "w")
                file.write("".join(booklist))
                click.echo("%s was returned to the library" %name)
                file.close()
                return
        click.echo("%s not found, try print-booklist command to see available books" % name)
        return

@click.command()
@click.argument("file", type=click.File('r'), default='personal_library.txt')
def print_booklist(file):
    """Prints the entire list of books. With return dates for books lent"""
    booklist = file.read()
    click.echo(booklist)

cli.add_command(add_book)
cli.add_command(delete_book)
cli.add_command(lend_book)
cli.add_command(return_book)
cli.add_command(print_booklist)

if __name__ == '__main__':
    cli()
