import subprocess
import sys

def run(command: str, error_message: str = None):
    """
    Runs a shell command, handles errors, and provides optional custom error messages.

    Args:
        command (str): The shell command to execute.
        error_message (str, optional): A custom message to display if the command fails.
                                       Defaults to None.
    """
    try:
        # shell=True is used for convenience in startup scripts to run commands
        # as they would be typed in a shell.
        # capture_output=True captures stdout and stderr.
        # text=True decodes stdout and stderr as text.
        # check=True raises a CalledProcessError if the command returns a non-zero exit code.
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
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

if __name__ == "__main__":
    # Example usage:
    print("Running a successful command:")
    run("echo 'Hello from run function!'")

    print("\nRunning a failing command:")
    # This command will fail, and the custom error message will be displayed
    run("ls non_existent_directory", error_message="Failed to list directory because it does not exist.")
