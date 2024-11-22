import argparse
from app.books.service import BookService
from app.setups import engine


class Subcommand:
    @staticmethod
    def InitParser(subparsers: argparse._SubParsersAction):
        raise Exception()


class ToJson(Subcommand):
    @staticmethod
    def Command(args):
        filename = args.filename
        BookService.ExportToJson(engine, filename)

    @staticmethod
    def InitParser(subparsers: argparse._SubParsersAction):
        subprog = subparsers.add_parser("export",
                                        help="export database to json")
        subprog.add_argument("filename",
                             help="the name of the file to export")
        subprog.set_defaults(func=ToJson.Command)


class Add(Subcommand):
    @staticmethod
    def Command(args):
        title = args.title
        author = args.author
        year = args.year
        BookService.AddBook(engine, title, author, year)
        print(f"The book '{title}' by {author} has been successfully added")

    @staticmethod
    def InitParser(subparsers: argparse._SubParsersAction):
        subprog = subparsers.add_parser("add",
                                        help="add a new book to the database")
        subprog.add_argument("title",
                             help="the title of the book")
        subprog.add_argument("author",
                             help="the author of the book")
        subprog.add_argument("year",
                             type=int,
                             help="the year of the book's publication")
        subprog.set_defaults(func=Add.Command)


class Delete(Subcommand):
    @staticmethod
    def Command(args):
        id = args.id
        delete_candidates = BookService.FindAll(engine, id=id)
        BookService.DeleteById(engine, id)
        print("The following books have been successfully deleted: ")
        print("\n".join(map(str, delete_candidates)))

    @staticmethod
    def InitParser(subparsers: argparse._SubParsersAction):
        subprog = subparsers.add_parser("delete",
                                        help="delete a book from the database")
        subprog.add_argument("id",
                             type=int,
                             help="id of the book to delete")
        subprog.set_defaults(func=Delete.Command)


class Search(Subcommand):
    @staticmethod
    def Command(args):
        filters = dict()
        if args.title:
            filters.update({"title": args.title})
        if args.author:
            filters.update({"author": args.author})
        if args.year:
            filters.update({"year": args.year})
        res = BookService.FindAll(engine, **filters)
        print("The following books were successfully found:")
        print("\n".join(map(str, res)))

    @staticmethod
    def InitParser(subparsers: argparse._SubParsersAction):
        subprog = subparsers.add_parser("search",
                                        help="find the books in the database")
        subprog.add_argument("-t", "--title",
                             help="the title of the book")
        subprog.add_argument("-a", "--author",
                             help="the author of the book")
        subprog.add_argument("-y", "--year",
                             type=int,
                             help="the year of the book's publication")
        subprog.set_defaults(func=Search.Command)


class Show(Subcommand):
    @staticmethod
    def Command(args):
        res = BookService.FindAll(engine)
        print("\n".join(map(str, res)))

    @staticmethod
    def InitParser(subparsers: argparse._SubParsersAction):
        subprog = subparsers.add_parser(
            "show",
            help="show all books from the database")
        subprog.set_defaults(func=Show.Command)


class UpdateStatus(Subcommand):
    @staticmethod
    def Command(args):
        id = args.id
        status = args.status
        BookService.UpdateStatus(engine, id, status)
        print("The record has been updated:")
        updated_fields = BookService.FindAll(engine, id=id)
        print("\n".join(map(str, updated_fields)))

    @staticmethod
    def InitParser(subparsers: argparse._SubParsersAction):
        subprog = subparsers.add_parser("update_status",
                                        help="update the status of the book")
        subprog.add_argument("id",
                             type=int,
                             help="id of the book to update")
        subprog.add_argument("status",
                             choices=("в наличии", "выдана"),
                             help="the new status of the book")
        subprog.set_defaults(func=UpdateStatus.Command)
