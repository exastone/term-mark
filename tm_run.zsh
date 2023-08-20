function tm_run() {
    # Check if an argument is provided
    if [ -z "$1" ]; then
        echo "Missing argument. Usage: tm_run <argument>"
        return 1
    fi

    # run term-mark
    eval "source $HOME/Dev/term-mark/venv/bin/activate && python $HOME/Dev/term-mark/main.py $1"

    # deactivate venv
    eval "deactivate"

    # File of commands to run
    filename="$HOME/.tmp/termmark.tmp"

    # Check if the file exists
    if [ ! -f "$filename" ]; then
        echo "File $filename not found."
        return 1
    fi

    # Read the first command from the file
    read -r command < "$filename"

    # Delete the tmp file
    rm "$filename"

    # Execute the command
    eval "$command"
    if [ $? -ne 0 ]; then
        echo "Error executing: $command"
    fi
}