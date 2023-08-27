# term-mark • bookmarks for your terminal 📚

Bookmark directories to quickly jump to them later, no more tabbing through directories!

![Jump to path](https://github.com/exastone/term-mark/blob/dev/assets/demo-mark-long-path.gif)

## Install

`pip install term-mark`

Because python cannot interact with the terminal outside of the interpeter any directory changes to the terminal will
revert after the program terminates, to make term-mark work you need to wrap the program execution in a shell function that runs
term-mark which can facilitate directory navigation.

term-mark handles the setup for you, but before you can use `tm` you need to run:

`term-mark --init`

This creates a shell function `tm.zsh` in `$HOME/.config/zsh/zsh_functions` and sources it your .zshrc file.

One last thing: you'll likely need to reload your .zshrc file

`source $HOME/.zshrc`

You can now use term-mark with `tm`!

## Usage

- Bookmark (toggle) the current directory: `tm -M` or `tm --mark`
- Show bookmarks: `tm -S` or `tm --show`
- Remove bookmarks (interactive) menu: `tm -R` or `tm --remove`

You can use `tm --find <base dir> [--depth <number>]` to search and add bookmarks for project directories (idenitifed by .git folder) under the base path provided.

e.g. you can run `tm --find ~/dev` (--depth 2 is default)
to automatically add bookmarks to **AudioVis**, **Bake**, **DSIM** directories

```
./dev
├── AudioVis            [bookmark added for `AudioVis`]
│   ├── .git            [<- .git found]
│   └── ...
├── Bake                [bookmark added for `Bake`]
│   ├── .git            [<- .git found]
│   └── ...
│   ├── src             [bookmark NOT added `/Bake/src`]
│   |   └── ...
│   └── .vscode         [bookmark NOT added `.vscode`]
│       └── ...
├── GO
│   └── DSIM            [bookmark added for `DSIM`]
│       ├── .git        [<- .git found]
│       ├── .vscode
|       |   └── ...
│       └── ...
└── ...
```

## Uninstall

`pip uninstall term-mark`

Delete the shell function:

`rm $HOME/.config/zsh/zsh_functions/tm.zsh`

If you don't have anything else in this directory you can also delete the entire directory:

`rm -r $HOME/.config/zsh/`

Remove the following line from your .zshrc file:

`source "$HOME/.config/zsh/zsh_functions/tm.zsh"`

There's only 2 dependencies for term-mark, `pfzy` and `prompt-toolkit`
If you're sure these dependencies aren't used by another package you can also pip install these for a completely clean
uninstall.

## Attribution

This CLI tool includes code and components from the [InquirerPy](https://github.com/kazhala/InquirerPy) package created
by kazhala, specifically a fork from [Gracer](https://github.com/Gracecr/InquirerPy)

InquirerPy is a powerful Python library for creating interactive command-line interfaces.
