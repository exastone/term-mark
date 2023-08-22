function tm_run() {
    # Check if an argument is provided
    if [ -z "$1" ]; then
        echo "Missing argument. Usage: tm_run <argument>"
        return 1
    fi

    local show_option=false

    # Check if the option provided is "-S" or "--show"
    if [ "$1" = "-S" ] || [ "$1" = "--show" ]; then
        show_option=true
        # shift  # Remove the option from the arguments
    fi


    # run term-mark
    eval "source $HOME/Dev/term-mark/venv/bin/activate && python $HOME/Dev/term-mark/main.py $1 $2"
    python_exit_status=$?  # Capture the exit status of the Python program

    # deactivate venv
    eval "deactivate"

    # File of commands to run
    filename="$HOME/.tmp/termmark.tmp"

    # Execute the command if the show_option is true
    # if [ "$show_option" = true ]; then

    # Execute the command if the show_option is true and Python exit status is 0
    if [ "$show_option" = true ] && [ "$python_exit_status" -eq 0 ]; then
        # Check if the file exists
        if [ ! -f "$filename" ]; then
            echo "File $filename not found."
            return 1
        fi

        # Read the first command from the file
        read -r command < "$filename"

        # Delete the file (cleanup)
        rm "$filename"

        # Execute the command
        eval "$command"
        if [ $? -ne 0 ]; then
            echo "Error executing: $command"
        fi
    fi
}
