# term-mark • bookmarks for your terminal 📚

Bookmark directories to quickly jump to them later

![Jump to path](https://github.com/exastone/term-mark/blob/dev/assets/demo-mark-long-path.gif)

# Install

`pip install term-mark`

Because python cannot directly write to a terminals input buffer (stdin) and any directory changes to the terminal will
revert after the
program terminates, to make term-mark work you need to wrap the program execution in a shell function that runs
term-mark which can facilitate directory navigation.

After term-mark is installed through pip, add the following create the following function and source it to your .zshrc
or
.bashrc

```shell
function tm() {
    # Check if an argument is provided
    if [ -z "$1" ]; then
        echo "Missing argument. Usage: tm_run <argument>"
        return 1
    fi
    local show_option=false
    # Check if the option provided is "-S" or "--show"
    if [ "$1" = "-S" ] || [ "$1" = "--show" ]; then
        show_option=true
    fi
    # run term-mark
    eval "term-mark $1 $2"
    python_exit_status=$?  # Capture the exit status of the Python program
    # File of commands to run
    filename="$HOME/.tmp/termmark.tmp"
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
```

Add the following line to your .zshrc (or .bashrc) file:
`source "$HOME/.config/zsh/zsh_functions/tm.zsh"`
replace *.config/zsh/zsh_functions* with the path to `tm` shell function.

