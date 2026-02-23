#!/usr/bin/env python3
"""
dotnote: A secure note-making CLI tool (root-only)
"""

import argparse
import sqlite3
import os
import sys
from rich.console import Console
from rich.table import Table

DB_PATH = "/root/notes.db"



def require_root():
    if os.geteuid() != 0:
        print("❌ Permission denied")
        print("🔒 This tool requires root privileges to run.")
        print("👉 Try: sudo dotnote <command>")
        sys.exit(1)




def init(args):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            note TEXT NOT NULL,
            tags TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("✅ Table created successfully")


def add_note(args):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    tags_str = None
    if args.tags:
        tags = [tag.strip() for tag in args.tags.split(",")]
        tags_str = ",".join(tags)

    c.execute(
        "INSERT INTO notes (note, tags) VALUES (?, ?)",
        (args.note, tags_str)
    )
    conn.commit()
    conn.close()

    print("✅ Note added successfully")

    if args.show:
        view_notes(args)


def view_notes(args):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM notes")
    notes = c.fetchall()
    conn.close()

    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=4)
    table.add_column("Note")
    table.add_column("Tags", style="dim")

    all_tags = set()

    for note in notes:
        tags = note[2] or ""
        tag_list = [t.strip() for t in tags.split(",") if t]
        all_tags.update(tag_list)
        table.add_row(str(note[0]), note[1], ", ".join(tag_list))

    console.print("\n📒 Your notes:\n")
    console.print(table)

    if all_tags:
        console.print("\n🏷 All tags:")
        for tag in sorted(all_tags):
            console.print(f"- {tag}")


def delete_notes(args):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if args.all:
        confirm = input(
            "⚠ WARNING: This will DELETE ALL notes permanently!\n"
            "Type YES to continue: "
        )
        if confirm != "YES":
            print("❌ Operation cancelled")
            conn.close()
            return

        # Delete all notes
        c.execute("DELETE FROM notes")

        # RESET AUTOINCREMENT COUNTER
        c.execute("DELETE FROM sqlite_sequence WHERE name='notes'")

        conn.commit()
        conn.close()
        print("✅ All notes deleted (ID reset to 1)")
        return

    elif args.tag:
        c.execute("DELETE FROM notes WHERE tags LIKE ?", (f"%{args.tag}%",))
        print(f"✅ Notes with tag '{args.tag}' deleted")

    elif args.id:
        c.execute("DELETE FROM notes WHERE id = ?", (args.id,))
        print(f"✅ Note with ID {args.id} deleted")

    conn.commit()
    conn.close()


def search_notes(args):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM notes")
    notes = c.fetchall()
    conn.close()

    query = args.query.lower()

    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=4)
    table.add_column("Note")
    table.add_column("Tags", style="dim")

    for note in notes:
        if query in note[1].lower() or (note[2] and query in note[2].lower()):
            table.add_row(str(note[0]), note[1], note[2] or "")

    console.print(f"\n🔍 Notes containing '{args.query}':\n")
    console.print(table)




parser = argparse.ArgumentParser(
    description="dotnote: Secure root-only note CLI",
    formatter_class=argparse.RawTextHelpFormatter
)

subparsers = parser.add_subparsers(required=True)


# init
init_parser = subparsers.add_parser(
    "init",
    help="Create notes table",
    epilog="Example:\n  sudo dotnote init"
)
init_parser.set_defaults(func=init)


# add
add_parser = subparsers.add_parser(
    "add",
    help="Add a new note",
    formatter_class=argparse.RawTextHelpFormatter,
    epilog="""Examples:
  sudo dotnote add "This is a new note"
  sudo dotnote add "This is a new note" -t "tag1, tag2"
"""
)
add_parser.add_argument("note", help="Note content")
add_parser.add_argument("-t", "--tags", help="Comma-separated tags")
add_parser.add_argument("-s", "--show", action="store_true", help="Show notes after adding")
add_parser.set_defaults(func=add_note)


# view
view_parser = subparsers.add_parser(
    "view",
    help="View all notes",
    epilog="Example:\n  sudo dotnote view"
)
view_parser.set_defaults(func=view_notes)


# delete
delete_parser = subparsers.add_parser(
    "delete",
    help="Delete notes",
    formatter_class=argparse.RawTextHelpFormatter,
    epilog="""Examples:
  sudo dotnote delete -i 3
  sudo dotnote delete -t "tag1"
  sudo dotnote delete -a   (⚠ deletes ALL notes)
"""
)

delete_group = delete_parser.add_mutually_exclusive_group(required=True)
delete_group.add_argument("-a", "--all", action="store_true", help="Delete ALL notes")
delete_group.add_argument("-t", "--tag", help="Delete notes by tag")
delete_group.add_argument("-i", "--id", type=int, help="Delete note by ID")

delete_parser.set_defaults(func=delete_notes)


# search
search_parser = subparsers.add_parser(
    "search",
    help="Search notes",
    epilog="Example:\n  sudo dotnote search linux"
)
search_parser.add_argument("query", help="Search keyword")
search_parser.set_defaults(func=search_notes)


# execute

require_root()
args = parser.parse_args()
args.func(args)
