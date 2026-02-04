The `setup_cli.py` script has been updated to include functions for installing `zsh-syntax-highlighting`, `zsh-autosuggestions`, `zsh-vi-mode`, and `fzf`. These functions will clone the respective repositories into the Oh My Zsh custom plugins directory and run any necessary install scripts.

Additionally, the `dotfiles/zshrc/.zshrc` file was updated to include these plugins in the `plugins` array:
`plugins=(git zsh-syntax-highlighting zsh-autosuggestions zsh-vi-mode)`
