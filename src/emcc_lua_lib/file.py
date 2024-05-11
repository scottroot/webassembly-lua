import os


class LuaFile():
    """
    Represents a Lua file used as part of a build script to compile Lua to
    WebAssembly (Wasm).

    Attributes:
        filepath (str): The path to the Lua file.
        basename (str): The base name of the Lua file.
        module_name (str): The name of the Lua module derived from file name.
    """

    def __init__(self, filepath, basename=None):
        """
        Initializes a LuaFile instance.

        Args:
            filepath (str): The path to the Lua file.
            basename (str, optional): The base name of the Lua file.
                If not provided, it's extracted from the filepath.
        """
        self.filepath = filepath
        if basename:
            self.basename = basename
        else:
            self.basename = os.path.basename(filepath)

        module_name = os.path.splitext(self.basename)[0].replace("/", ".")
        if module_name.startswith(".src"):
            module_name = module_name.replace(".src", "", 1)
        self.module_name = module_name


class ModuleFile():
    """
    Represents a module file used in Lua to WebAssembly (Wasm) conversion.

    Attributes:
        filepath (str): The path to the module file.
        module_name (str): The name of the Lua module.
        basename (str): The base name of the module file.
    """

    def __init__(self, filepath, luaopen_name):
        """
        Initializes a ModuleFile instance.

        Args:
            filepath (str): The path to the module file.
            luaopen_name (str): The name of the Lua module.
        """
        self.filepath = filepath
        self.module_name = luaopen_name
        self.basename = luaopen_name.replace("_", ".")


class BundleFile(LuaFile):
    """
    Represents a bundled Lua file used as part of a build script to compile Lua
    to WebAssembly (Wasm).

    Attributes:
        filepath (str): The relative path to the bundled Lua file.
        basename (str): The base name of the bundled Lua file.
        module_name (str): The name of the Lua module derived from file name.
    """

    def __init__(self, filepath):
        """
        Initializes a BundleFile instance.

        Args:
            filepath (str): The path to the bundled Lua file.
        """
        super().__init__(filepath)
        self.filepath = os.path.relpath(filepath)
