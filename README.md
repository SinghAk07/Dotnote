<h1 align="center">
    DOTNOTE
  <br>
</h1>

<h4 align="center">DOTNOTE is a utility for note management and search from your terminal</h4>


![Dotnote](https://github.com/SinghAk07/Dotnote/blob/2100b32b032bb194c856282fc0490c074fd70649/proof.png)


## ✨ Features

- Store notes locally using SQLite
- Organize notes using tags
- Search notes by keywords (notes and tags)
- Delete notes by ID, tag, or all at once
- Confirmation prompt before deleting all notes
- Automatically reset note IDs after full deletion
- Root-only access for privacy and security

## 📋 Requirements

- Python 3.x
- argparse
- sqlite3
- rich

Install `rich` if required:

```sh
pip3 install rich
```

## 🏗️ Installation

```sh
git clone https://github.com/SinghAk07/Dotnote
cd Dotnote
sudo chmod +x setup.sh
./setup.sh
```

## 🔒 Why Root Access Is Required

dotnote stores notes securely at:

```
/root/notes.db
```

Running as root ensures privacy and prevents other users from accessing or modifying notes.

If run without root privileges:

```
❌ Permission denied
🔒 This tool requires root privileges to run.
👉 Try: sudo dotnote <command>
```

## ⛏️ Usage

```sh
sudo dotnote [subcommand] [options]
```

## 🔧 Subcommands

| Subcommand | Description |
|-----------|-------------|
| init | Create the notes database |
| add | Add a new note |
| view | View all notes |
| delete | Delete notes |
| search | Search notes |

## 📌 Examples

### Initializing the Database

```sh
dotnote init
```

### Adding a Note

```sh
dotnote add "This is a new note" -t "tag1, tag2"
```

### Viewing Notes

```sh
dotnote view
```

### Deleting Notes

```sh
dotnote delete [options]
```

- Delete all notes with a specific tag:

```sh
dotnote delete -t "tag1"
```

- Delete all notes:

```sh
dotnote delete -a
```

- Delete note with specified ID:

```sh
dotnote delete -i 3
```

### Searching Notes

```sh
dotnote search "keyword"
```

