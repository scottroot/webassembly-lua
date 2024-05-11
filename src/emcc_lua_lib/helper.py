import os
import subprocess

IS_DEBUG = os.environ.get("DEBUG", "")


def encode_hex_literals(source: str) -> str:
    """
    Encodes a string into a comma-separated list of hexadecimal literals.

    Args:
        source (str): The input string to encode.

    Returns:
        str: Comma-separated list of hexadecimal literals representing input.
    """
    return ", ".join([f"0x{x:02x}" for x in source.encode("utf-8")])


def get_extension(file: str) -> str:
    """
    Retrieves the extension of a file.

    Args:
        file (str): The path to the file.

    Returns:
        str: The extension of the file.
    """
    return os.path.splitext(os.path.basename(file))[1][1:]


def is_lua_source_file(file: str) -> bool:
    """
    Checks if a file is a Lua source file.

    Args:
        file (str): The path to the file.

    Returns:
        bool: True if the file is a Lua source file, else False.
    """
    ext = get_extension(file)
    return ext in ["lua", "luac"]


def is_binary_library(file: str) -> bool:
    """
    Checks if a file is a binary library file.

    Args:
        file (str): The path to the file.

    Returns:
        bool: True if the file is a binary library file, else False.
    """
    ext = get_extension(file)
    return ext in ["o", "a", "so", "dylib"]


def shell_exec(*cmd_args: str) -> tuple[str, int]:
    """
    Executes a shell command and captures its output.

    Args:
        *cmd_args: The command and its arguments.

    Returns:
        tuple: (output of the command, the return code)
    """
    commands = list(cmd_args)
    try:
        proc = subprocess.run(commands, stdout=subprocess.PIPE, check=True)
        return proc.stdout.decode("utf-8").strip("\n"), proc.returncode
    except subprocess.CalledProcessError as e:
        print(f"Failed running shell_exec: {e}")
        return None, e.returncode


def debug_print(*args, **kwargs) -> None:
    """
    Prints debug messages if the DEBUG environment variable is set.

    Args:
        *args: The objects to print.
        **kwargs: Keyword arguments to pass to the print function.
    """
    if IS_DEBUG:
        print(*args)
