import subprocess
import sys
import os
import getpass
import argparse

def run(command: str, error_message: str = None, dry_run: bool = False, password: str = None, dir_path: str = None):
    """
    Runs a shell command, handles errors, and provides optional custom error messages.
    Can also handle commands requiring sudo by piping a password to stdin.

    Args:
        command (str): The shell command to execute.
        error_message (str, optional): A custom message to display if the command fails.
                                       Defaults to None.
        dry_run (bool): If True, print the command but do not execute it.
        password (str, optional): The password to use for commands requiring sudo or chsh.
        dir_path (str, optional): The directory to run the command in. Defaults to current.
    """
    if dry_run:
        print(f"[Dry Run] Would execute: {command} in {dir_path if dir_path else os.getcwd()}")
        return

    process_input = None
    # For sudo commands, we echo the password and pipe it to sudo -S
    if password and command.startswith("sudo"):
        command = f"echo {password} | sudo -S {command}"
    # For chsh, it expects the password on stdin directly
    elif password and "chsh" in command:
        process_input = password + '\n' # chsh expects password followed by a newline

    try:
        # shell=True is used for convenience in startup scripts to run commands
        # as they would be typed in a shell.
        # capture_output=True captures stdout and stderr.
        # text=True decodes stdout and stderr as text.
        # check=True raises a CalledProcessError if the command returns a non-zero exit code.
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True, input=process_input, cwd=dir_path)
        if result.stdout:
            print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        if error_message:
            print(f"Error: {error_message}", file=sys.stderr)
        print(f"Command '{e.cmd}' failed with exit code {e.returncode}.", file=sys.stderr)
        if e.stdout:
            print(f"Stdout:\n{e.stdout.strip()}", file=sys.stderr)
        if e.stderr:
            print(f"Stderr:\n{e.stderr.strip()}", file=sys.stderr)
        sys.exit(1)

def is_command_available(command: str) -> bool:
    """Checks if a command is available in the system's PATH."""
    # Using 'command -v' is more portable than 'type' for checking command existence
    return subprocess.call(f"command -v {command}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

def install_rust(dry_run: bool = False, password: str = None):
    """Installs Rust using rustup if not already installed."""
    print("--- Installing Rust ---")
    if is_command_available("rustc"):
        print("Rust is already installed.")
        return

    print("Downloading and installing Rust...")
    run("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y",
        error_message="Failed to install Rust.", dry_run=dry_run, password=password)
    print("Rust installation command issued.")
    # Note: rustup itself will configure the PATH in .bashrc/.zshrc.
    # For the current script execution, we don't need to modify os.environ["PATH"]
    # as the `run` calls don't depend on cargo directly after installation.

def setup_oh_my_zsh(dry_run: bool = False, password: str = None):
    """Sets up Zsh and Oh My Zsh if not already configured."""
    print("--- Setting up Oh My Zsh ---")

    # Check if Zsh is installed
    if not is_command_available("zsh"):
        print("Zsh not found. Installing Zsh...")
        # Assuming Debian/Ubuntu-like system for apt
        run("sudo apt update && sudo apt install -y zsh", error_message="Failed to install Zsh.", dry_run=dry_run, password=password)
    else:
        print("Zsh is already installed.")

    # Check if Oh My Zsh is installed
    if os.path.exists(os.path.expanduser("~/.oh-my-zsh")):
        print("Oh My Zsh is already installed.")
    else:
        print("Installing Oh My Zsh...")
        # The unattended install script prevents opening a new zsh shell immediately
        run('sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended',
            error_message="Failed to install Oh My Zsh.", dry_run=dry_run, password=password)
        print("Oh My Zsh installation command issued.")

    # Set Zsh as default shell if not already
    current_shell = os.environ.get("SHELL")
    # Check if current_shell ends with zsh, as path might vary (/usr/bin/zsh, /bin/zsh, etc.)
    if not current_shell or not current_shell.endswith("zsh"):
        print("Setting Zsh as default shell...")
        run('chsh -s $(which zsh)', error_message="Failed to set Zsh as default shell.", dry_run=dry_run, password=password)
        if not dry_run:
            print("\n------------------------------------------------------------")
            print("IMPORTANT: Zsh has been set as your default shell.")
            print("For this change to take full effect, you MUST log out of your current session")
            print("and log back in. New terminals opened before logging out will still use your old shell.")
            print("------------------------------------------------------------")
    else:
        print("Zsh is already the default shell.")

def install_gemini_cli(dry_run: bool = False, password: str = None):
    """Installs NVM, Node.js (LTS), and Gemini CLI."""
    print("--- Setting up Gemini CLI ---")

    NVM_DIR = os.path.expanduser("~/.nvm")
    NVM_SH = os.path.join(NVM_DIR, "nvm.sh")

    # Check for nvm installation
    if not os.path.exists(NVM_SH):
        print("NVM not found. Installing NVM...")
        # Install NVM
        # The official nvm install script automatically adds sourcing to shell config files.
        # For the current session, we will manually source it after installation.
        run("curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash",
            error_message="Failed to install NVM.", dry_run=dry_run)
        if not dry_run:
            print("NVM installation command issued. Attempting to source NVM for current session...")
            # For the current script to use nvm, we need to source it.
            # This is tricky because `subprocess.run` creates a new shell.
            # We'll prepend sourcing to subsequent commands that use nvm.
    else:
        print("NVM is already installed.")

    # Source NVM for the current command execution context and install Node.js LTS
    NVM_SOURCE_CMD = f'export NVM_DIR="{NVM_DIR}" && [ -s "{NVM_SH}" ] && . "{NVM_SH}" && '

    print("Installing Node.js (LTS) using NVM...")
    run(NVM_SOURCE_CMD + "nvm install --lts",
        error_message="Failed to install Node.js LTS.", dry_run=dry_run)

    print("Setting Node.js (LTS) as default using NVM...")
    run(NVM_SOURCE_CMD + "nvm use --lts",
        error_message="Failed to set Node.js LTS as default.", dry_run=dry_run)

    # Install gemini-cli
    print("Installing @google/gemini-cli globally...")
    if is_command_available("gemini"):
        print("@google/gemini-cli is already installed.")
    else:
        run(NVM_SOURCE_CMD + "npm install -g @google/gemini-cli",
            error_message="Failed to install @google/gemini-cli.", dry_run=dry_run)
        print("Gemini CLI setup command issued.")

def install_stow(dry_run: bool = False, password: str = None):
    """Installs GNU Stow if not already installed."""
    print("--- Installing GNU Stow ---")
    if is_command_available("stow"):
        print("GNU Stow is already installed.")
        return

    print("Installing GNU Stow...")
    run("sudo apt update && sudo apt install -y stow",
        error_message="Failed to install GNU Stow.", dry_run=dry_run, password=password)
    print("GNU Stow installation command issued.")

def install_powerlevel10k(dry_run: bool = False, password: str = None):
    """Installs Powerlevel10k theme for Oh My Zsh."""
    print("--- Installing Powerlevel10k ---")
    p10k_dir = os.path.expanduser("~/.oh-my-zsh/custom/themes/powerlevel10k")

    if os.path.exists(p10k_dir):
        print("Powerlevel10k is already installed.")
        return

    print("Cloning Powerlevel10k repository...")
    run(f"git clone --depth=1 https://github.com/romkatv/powerlevel10k.git {p10k_dir}",
        error_message="Failed to clone Powerlevel10k repository.", dry_run=dry_run, password=password)
    print("Powerlevel10k cloning command issued.")

def install_oh_my_zsh_plugins(dry_run: bool = False, password: str = None):
    """Installs specified Oh My Zsh plugins."""
    print("--- Installing Oh My Zsh Plugins ---")
    plugins_dir = os.path.expanduser("~/.oh-my-zsh/custom/plugins")
    
    # Ensure the plugins directory exists
    run(f"mkdir -p {plugins_dir}", dry_run=dry_run)

    plugins_to_install = {
        "zsh-syntax-highlighting": "https://github.com/zsh-users/zsh-syntax-highlighting.git",
        "zsh-autosuggestions": "https://github.com/zsh-users/zsh-autosuggestions",
        "zsh-vi-mode": "https://github.com/jeffreytse/zsh-vi-mode.git",
    }

    for plugin_name, repo_url in plugins_to_install.items():
        plugin_path = os.path.join(plugins_dir, plugin_name)
        if os.path.exists(plugin_path):
            print(f"{plugin_name} is already installed.")
        else:
            print(f"Cloning {plugin_name} repository...")
            run(f"git clone --depth=1 {repo_url} {plugin_path}",
                error_message=f"Failed to clone {plugin_name} repository.", dry_run=dry_run, password=password)
            print(f"{plugin_name} cloning command issued.")
    print("Oh My Zsh plugin installation commands issued.")

def install_fzf(dry_run: bool = False, password: str = None):
    """Installs fzf (fuzzy finder)."""
    print("--- Installing fzf ---")
    fzf_dir = os.path.expanduser("~/.fzf")

    # check if fzf is already installed
    if os.path.exists(fzf_dir):
        print("fzf is already installed in ~/.fzf.")
        return

    print("Cloning fzf repository...")
    run(f"git clone --depth 1 https://github.com/junegunn/fzf.git {fzf_dir}",
        error_message="Failed to clone fzf repository.", dry_run=dry_run, password=password)
    
    print("Running fzf install script...")
    # The install script is interactive by default, use --all to bypass some prompts
    # and --no-bash-completion, --no-fish-completion, --no-key-bindings
    # because oh-my-zsh handles completion and key bindings via its plugin system.
    # However, the user might want these, so let's use the default install script without arguments
    # and let the user interact if --dry-run is false.
    # For a fully automated script, it's better to explicitly list the options, but for now,
    # just running install script.
    run(f"{fzf_dir}/install --key-bindings --completion --no-update-rc",
        error_message="Failed to run fzf install script.", dry_run=dry_run, password=password)
    print("fzf installation command issued.")

def setup_dotfiles_with_stow(dry_run: bool = False, password: str = None):
    """Sets up dotfiles using GNU Stow."""
    print("--- Setting up Dotfiles with Stow ---")
    install_stow(dry_run=dry_run, password=password)

    # Assuming dotfiles directory is a sibling of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dotfiles_path = os.path.join(script_dir, "dotfiles")

    if not os.path.isdir(dotfiles_path):
        print(f"Error: Dotfiles directory not found at {dotfiles_path}", file=sys.stderr)
        return

    print(f"Stowing dotfiles from {dotfiles_path}...")
    
    # Stow p10k
    print("Stowing p10k configuration...")
    # Using -R (restow) to handle cases where links might already exist or conflict
    run("stow -R -t ~ p10k", dir_path=dotfiles_path, error_message="Failed to stow p10k.", dry_run=dry_run, password=password)

    # Stow zshrc (will only work if dotfiles/zshrc exists)
    zshrc_package_path = os.path.join(dotfiles_path, "zshrc")
    if os.path.isdir(zshrc_package_path):
        print("Stowing zshrc configuration...")
        run("stow -R -t ~ zshrc", dir_path=dotfiles_path, error_message="Failed to stow zshrc.", dry_run=dry_run, password=password)
    else:
        print(f"Skipping zshrc stow: '{zshrc_package_path}' not found. Create this directory with your .zshrc inside to stow it.")

    # Stow git config
    git_package_path = os.path.join(dotfiles_path, "git")
    if os.path.isdir(git_package_path):
        print("Stowing git configuration...")
        run("stow -R -t ~ git", dir_path=dotfiles_path, error_message="Failed to stow git.", dry_run=dry_run, password=password)
    else:
        print(f"Skipping git stow: '{git_package_path}' not found.")

    # Stow astronvim (will only work if dotfiles/astronvim exists)
    astronvim_package_path = os.path.join(dotfiles_path, "astronvim")
    if os.path.isdir(astronvim_package_path):
        print("Stowing astronvim configuration...")

        # Ensure ~/.config/nvim exists
        nvim_config_target_dir = os.path.expanduser("~/.config/nvim")
        if not os.path.exists(nvim_config_target_dir):
            print(f"Creating directory: {nvim_config_target_dir}")
            run(f"mkdir -p {nvim_config_target_dir}", dry_run=dry_run)
            
        # AstroNvim config lives in ~/.config/nvim
        run("stow -R -t ~/.config/nvim astronvim", dir_path=dotfiles_path, error_message="Failed to stow astronvim.", dry_run=dry_run, password=password)
    else:
        print(f"Skipping astronvim stow: '{astronvim_package_path}' not found. Create this directory with your AstroNvim config inside to stow it to ~/.config/nvim.")

    print("Dotfiles stowage commands issued.")

def install_nvim_and_astronvim(dry_run: bool = False, password: str = None):
    """Installs Neovim from latest GitHub AppImage into ~/software/ and ensures Git is available."""
    print("--- Setting up Neovim ---")

    # Ensure Git is installed (required for cloning and later for AstroNvim)
    if not is_command_available("git"):
        print("Git not found. Installing Git...")
        run("sudo apt update && sudo apt install -y git",
            error_message="Failed to install Git.", dry_run=dry_run, password=password)
    else:
        print("Git is already installed.")

    # jq is no longer needed for direct AppImage download
    # if not is_command_available("jq"):
    #     print("jq not found. Installing jq...")
    #     run("sudo apt update && sudo apt install -y jq",
    #         error_message="Failed to install jq.", dry_run=dry_run, password=password)
    # else:
    #     print("jq is already installed.")

    software_dir = os.path.expanduser("~/software")
    nvim_appimage_path = os.path.join(software_dir, "nvim")

    # Check if Neovim AppImage is already installed and executable in ~/software/nvim
    if os.path.exists(nvim_appimage_path) and os.access(nvim_appimage_path, os.X_OK):
        print("Neovim AppImage is already installed and executable in ~/software/nvim.")
    else:
        print("Downloading and installing latest stable Neovim AppImage from GitHub...")
        
        # Create ~/software directory if it doesn't exist
        run(f"mkdir -p {software_dir}", dry_run=dry_run)

        # Direct download of nvim-linux-x86_64.appimage
        # Assumes x86_64 architecture
        download_url = "https://github.com/neovim/neovim/releases/latest/download/nvim-linux-x86_64.appimage"
        
        run(f"curl -L {download_url} -o {nvim_appimage_path}",
            error_message="Failed to download Neovim AppImage.", dry_run=dry_run)

        # Make the AppImage executable
        run(f"chmod +x {nvim_appimage_path}",
            error_message="Failed to make Neovim AppImage executable.", dry_run=dry_run)
        
        print("Neovim AppImage installed from GitHub release.")
    
    print("Neovim and Git setup commands issued.")

def install_nerd_font(dry_run: bool = False, password: str = None):
    """Installs MesloLGS NF Nerd Font and checks if they are already cached."""
    print("--- Installing MesloLGS NF Nerd Font ---")

    font_dir = os.path.expanduser("~/.local/share/fonts/MesloLGS NF")
    font_files = [
        "MesloLGS NF Regular.ttf",
        "MesloLGS NF Bold.ttf",
        "MesloLGS NF Italic.ttf",
        "MesloLGS NF Bold Italic.ttf",
    ]
    
    # Check if all font files already exist
    all_fonts_exist = True
    if os.path.isdir(font_dir):
        for font_file in font_files:
            if not os.path.exists(os.path.join(font_dir, font_file)):
                all_fonts_exist = False
                break
    else:
        all_fonts_exist = False

    if all_fonts_exist:
        print("MesloLGS NF fonts are already installed and cached.")
        return

    print("Creating font directory...")
    run(f"mkdir -p \"{font_dir}\"", dry_run=dry_run)

    base_url = "https://github.com/romkatv/powerlevel10k-media/raw/master/"
    
    for font_file in font_files:
        # URL-encode the spaces in the font_file name
        encoded_font_file = font_file.replace(" ", "%20")
        download_url = f"{base_url}{encoded_font_file}"
        destination_path = os.path.join(font_dir, font_file) # Save with original filename
        print(f"Downloading {font_file}...")
        # Enclose destination_path in double quotes for curl -o
        run(f"curl -L '{download_url}' -o \"{destination_path}\"",
            error_message=f"Failed to download {font_file}.", dry_run=dry_run)

    print("Updating font cache...")
    run("fc-cache -fv", error_message="Failed to update font cache.", dry_run=dry_run)
    print("MesloLGS NF font installation commands issued.")

def install_docker(dry_run: bool = False, password: str = None):
    """Installs Docker using the convenience script and sets up user permissions."""
    print("--- Installing Docker ---")

    # Check if Docker is already installed by looking for 'docker' command
    if is_command_available("docker"):
        print("Docker is already installed.")
        # Check if current user is in the docker group
        try:
            subprocess.run("groups | grep -q docker", shell=True, check=True, text=True, capture_output=True)
            print("User is already in the 'docker' group.")
        except subprocess.CalledProcessError:
            print("User is not in the 'docker' group. Adding user to 'docker' group...")
            run("sudo usermod -aG docker $USER", error_message="Failed to add user to 'docker' group.", dry_run=dry_run, password=password)
            if not dry_run:
                print("\n------------------------------------------------------------")
                print("IMPORTANT: User added to 'docker' group.")
                print("For this change to take full effect, you MUST log out of your current session")
                print("and log back in. You will not be able to run docker commands without sudo until then.")
                print("------------------------------------------------------------")
        return

    print("Downloading and executing Docker convenience script...")
    # The convenience script itself handles installing docker-ce, containerd, and docker-compose-plugin
    run("curl -fsSL https://get.docker.com -o /tmp/get-docker.sh",
        error_message="Failed to download Docker convenience script.", dry_run=dry_run)
    run("sudo sh /tmp/get-docker.sh",
        error_message="Failed to execute Docker convenience script.", dry_run=dry_run, password=password)
    run("rm /tmp/get-docker.sh", error_message="Failed to remove Docker convenience script.", dry_run=dry_run)

    # Add the current user to the 'docker' group
    print("Adding current user to the 'docker' group...")
    run("sudo usermod -aG docker $USER", error_message="Failed to add user to 'docker' group.", dry_run=dry_run, password=password)
    if not dry_run:
        print("\n------------------------------------------------------------")
        print("IMPORTANT: Docker installed and user added to 'docker' group.")
        print("For this change to take full effect, you MUST log out of your current session")
        print("and log back in. You will not be able to run docker commands without sudo until then.")
        print("------------------------------------------------------------")
    print("Docker installation command issued.")

def install_utility_programs(dry_run: bool = False, password: str = None):

    cargo_programs = {
        "exa": "exa",
        "bottom": "btm",
        "watchexec-cli": "watchexec",
        "bat": "bat",
        "fd-find": "fd",
        "ripgrep": "rg",
        "tree-sitter-cli": "tree-sitter",
        "trunk": "trunk",
        "difftastic": "difft",
    }
    for package, command in cargo_programs.items():
        print(f"--- Installing {package} via cargo ---")
        if is_command_available(command):
            print(f"{package} (command: {command}) is already installed.")
        else:
            print(f"Installing {package}...")
            run(f"cargo install {package}",
                error_message=f"Failed to install {package} via cargo.", dry_run=dry_run)
            print(f"{package} installation command issued.")

    # apt packages

    apt_programs = [
        "wl-clipboard",
        "cmatrix",
        "neofetch",
        "htop",
        "tree",
        "python3-pip",
        "python3-venv",
        ]

    print("--- Installing utility programs via apt ---")
    for program in apt_programs:
        if is_command_available(program):
            print(f"{program} is already installed.")
        else:
            print(f"Installing {program}...")
            run(f"sudo apt update && sudo apt install -y {program}",
                error_message=f"Failed to install {program} via apt.", dry_run=dry_run, password=password)
            print(f"{program} installation command issued.")
    





if __name__ == "__main__":
    print("Starting CLI setup script...")
    
    parser = argparse.ArgumentParser(description="CLI setup script for Rust, Oh My Zsh, Gemini CLI, Powerlevel10k, and dotfiles.")
    parser.add_argument("--dry-run", action="store_true", help="If set, print commands but do not execute them.")
    args = parser.parse_args()

    # Get password once at the beginning if not in dry-run mode
    user_password = None
    if not args.dry_run:
        try:
            # Using getpass for secure password input
            user_password = getpass.getpass("Enter your password for sudo and chsh (will not be displayed): ")
        except EOFError:
            print("Password input cancelled.", file=sys.stderr)
            sys.exit(1)

    # Example usage of run function (from previous request)
    print("\n--- Testing run function ---")
    run("echo 'Hello from run function!'", dry_run=args.dry_run, password=user_password)
    print("--- End testing run function ---\
")

    install_rust(dry_run=args.dry_run, password=user_password)
    setup_oh_my_zsh(dry_run=args.dry_run, password=user_password)
    install_oh_my_zsh_plugins(dry_run=args.dry_run, password=user_password)
    install_fzf(dry_run=args.dry_run, password=user_password)
    install_gemini_cli(dry_run=args.dry_run, password=user_password)
    install_powerlevel10k(dry_run=args.dry_run, password=user_password)
    install_nvim_and_astronvim(dry_run=args.dry_run, password=user_password) # Install nvim and git
    setup_dotfiles_with_stow(dry_run=args.dry_run, password=user_password) # Stow dotfiles including astronvim
    install_nerd_font(dry_run=args.dry_run, password=user_password)
    install_utility_programs(dry_run=args.dry_run, password=user_password)
    install_docker(dry_run=args.dry_run, password=user_password)

    print("\nCLI setup script finished.")
    if args.dry_run:
        print("\nNOTE: This was a dry run. No changes were made to your system.")
        print("To perform the actual installation, remove the --dry-run flag and run the script again.")
