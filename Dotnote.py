#!/usr/bin/env python3

"""dotnote: A note Making CLI tool """

import argparse
import sqlite3
import re
from rich.console import Console
from rich.table import Table

def init(args):
    """Create a notes table in the database"""
    conn = sqlite3.connect("/root/notes.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 note TEXT,
                 tags TEXT)''')
    conn.commit()
    conn.close()
    print("Table Created Successfully 🎉")


def add_note(args):
    """Add a new note to the database"""
    conn = sqlite3.connect("/root/notes.db")
    c = conn.cursor()
    note = args.note
    tags = args.tags
    if tags:
        tags = tags.split(",")
        tags = [tag.strip() for tag in tags]
        tags_str = ",".join(tags)
    else:
        tags_str = None
    c.execute("INSERT INTO notes (note, tags) VALUES (?, ?)", (note, tags_str))
    conn.commit()
    print("Note added successfully ✅")
    if args.show:
        view_notes(args)
    conn.close()
