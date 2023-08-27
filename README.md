# term-mark • bookmarks for your terminal 📚

Bookmark directories to quickly jump to them later

![Jump to path](https://github.com/exastone/term-mark/blob/dev/assets/demo-mark-long-path.gif)

## Install

`pip install term-mark`

Because python cannot directly write to a terminals input buffer (stdin) and any directory changes to the terminal will
revert after the
program terminates, to make term-mark work you need to wrap the program execution in a shell function that runs
term-mark which can facilitate directory navigation.

term-mark handles the setup for you, but before you can use `tm` you need to run:

`term-mark --init`

This creates a shell function `tm.zsh` in `$HOME/.config/zsh/zsh_functions` and sources it your .zshrc file.

One last thing: you'll likely need to reload your .zshrc file

`source $HOME/.zshrc`

You can now use term-mark with `tm`!

## Uninstall

`pip uninstall term-mark`

Delete the shell function:

`rm $HOME/.config/zsh/zsh_functions/tm.zsh`

If you don't have anything else in this directory you can also delete the entire directory:

`rm -r $HOME/.config/zsh/`

Remove the following line from your .zshrc file:

`source "$HOME/.config/zsh/zsh_functions/tm.zsh"`

## Attribution

This CLI tool includes code and components from the [InquirerPy](https://github.com/kazhala/InquirerPy) package created
by kazhala, specifically a fork from [Gracer](https://github.com/Gracecr/InquirerPy)

InquirerPy is a powerful Python library for creating interactive command-line interfaces.
