#!/bin/bash

# Rename the dotnote.py file to dotnote
mv dotnote.py dotnote

# Move the dotnote file to /usr/local/bin
sudo mv dotnote /usr/local/bin/

# Make the dotnote file executable
sudo chmod +x /usr/local/bin/dotnote

# Remove the dotnote.pyc file if it exists
if [ -f dotnote.pyc ]; then
    rm dotnote.pyc
fi

echo "dotnote has been installed successfully! You can now use it from anywhere in the terminal by typing 'dotnote'"