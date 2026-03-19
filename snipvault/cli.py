import argparse
import sys
from . import vault


def main():
    parser = argparse.ArgumentParser(prog="snipvault", description="A simple snippet manager.")
    sub = parser.add_subparsers(dest="command", required=True)

    # add
    p_add = sub.add_parser("add", help="Add a snippet")
    p_add.add_argument("name", help="Snippet name")
    p_add.add_argument("snippet", help="Snippet content")
    p_add.add_argument("--tags", nargs="*", default=[], metavar="TAG", help="Optional tags")

    # get
    p_get = sub.add_parser("get", help="Retrieve a snippet")
    p_get.add_argument("name", help="Snippet name")

    # delete
    p_del = sub.add_parser("delete", help="Delete a snippet")
    p_del.add_argument("name", help="Snippet name")

    # list
    sub.add_parser("list", help="List all snippets")

    # search
    p_search = sub.add_parser("search", help="Search snippets")
    p_search.add_argument("query", help="Search query")

    args = parser.parse_args()

    if args.command == "add":
        vault.add(args.name, args.snippet, args.tags)
        print(f"Saved '{args.name}'.")

    elif args.command == "get":
        entry = vault.get(args.name)
        if entry is None:
            print(f"No snippet named '{args.name}'.", file=sys.stderr)
            sys.exit(1)
        print(entry["snippet"])
        if entry["tags"]:
            print(f"Tags: {', '.join(entry['tags'])}")

    elif args.command == "delete":
        if vault.delete(args.name):
            print(f"Deleted '{args.name}'.")
        else:
            print(f"No snippet named '{args.name}'.", file=sys.stderr)
            sys.exit(1)

    elif args.command == "list":
        data = vault.list_all()
        if not data:
            print("Vault is empty.")
        else:
            for name, entry in data.items():
                tags = f"  [{', '.join(entry['tags'])}]" if entry["tags"] else ""
                print(f"{name}{tags}")

    elif args.command == "search":
        results = vault.search(args.query)
        if not results:
            print("No matches.")
        else:
            for name, entry in results.items():
                tags = f"  [{', '.join(entry['tags'])}]" if entry["tags"] else ""
                print(f"{name}{tags}")
                print(f"  {entry['snippet'][:80]}")
