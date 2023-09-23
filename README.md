# term-mark • bookmarks for your terminal 📚

Bookmark directories to quickly jump to them later, no more tabbing through directories!

![Jump to path](https://github.com/exastone/term-mark/blob/dev/assets/demo-mark-long-path.gif)

## Install

> `pip install term-mark`

A shell function, 'tm.zsh' will be created in `$HOME/.config/zsh/zsh_functions` and appended as a source to your .zshrc file. 

**You'll likely need to reload your .zshrc file before using `tm`**

> `source $HOME/.zshrc`

You can now use term-mark with `tm` !

### Disable Glyphs

By default, glyphs are used for markers. If your shell doesn't support glyphs or your not using a 
patched font, you can disable glyphs by setting an environment variable which will use '●', '○' characters as fallback marker icons. i.e.

add `export TM_USE_GLYPHS=false` to your .zshrc file

run `source ~/.zshrc`

## Usage

- Bookmark (toggle) the current directory: `tm -M` / `--mark`
- Show bookmarks: `tm -S` / `--show`
- Remove bookmarks (interactive) menu: `tm -R` / `--remove`
    - useful for removing multiple bookmarks at the same time

**Auto-find & Add Bookmarks:**

You can use `tm --find <base dir> [--depth <number>]` to search and add bookmarks for project directories (idenitifed by .git folder) under the base path provided.

e.g. you can run `tm --find ~/dev` (--depth 2 is default)
to automatically add bookmarks to **dirA**, **dirB**, **dirC** directories

```
./dev
├── dirA          [bookmark added for `dirA`]
│   ├── .git            [<- .git found]
│   └── ...
├── dirB          [bookmark added for `dirB`]
│   ├── .git            [<- .git found]
│   ├── ...
│   ├── src             [bookmark NOT added `/dirB/src`]
│   |   └── ...
│   └── .vscode         [bookmark NOT added `.vscode`]
│       └── ...
├── GO
│   └── dirC      [bookmark added for `dirC`]
│       ├── .git        [<- .git found]
│       ├── .vscode
|       |   └── ...
│       └── ...
└── ...
```

## Uninstall

`pip uninstall term-mark`

Remove the following line from your .zshrc file:

`source "$HOME/.config/zsh/zsh_functions/tm.zsh"`

Delete the shell function:

`rm $HOME/.config/zsh/zsh_functions/tm.zsh`


There's only 2 dependencies for term-mark, `pfzy` and `prompt-toolkit`
If they're not used by another package you can also pip uninstall these for a completely clean
uninstall.

## Attribution

This CLI tool includes code and components from the [InquirerPy](https://github.com/kazhala/InquirerPy) package created
by kazhala, specifically a fork from [Gracer](https://github.com/Gracecr/InquirerPy)

InquirerPy is a powerful Python library for creating interactive command-line interfaces.
