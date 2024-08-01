import sysconfig
from typing import Tuple, TypeAlias

ScriptPathHome: TypeAlias = str
ScriptPathUser: TypeAlias = str
ScriptPathPrefix: TypeAlias = str


def get_script_paths() -> Tuple[ScriptPathHome, ScriptPathUser, ScriptPathPrefix]:
    """
    Get Python script installation paths

    virtualenv example:
    - Home: /Users/zach/.virtualenvs/chill_streams/bin
    - User: /Users/zach/Library/Python/3.12/bin
    - prefix: /Users/zach/.virtualenvs/chill_streams/bin

    Non-virtualenv (homebrew python) example:
    - Home: /opt/homebrew/opt/python@3.12/Frameworks/Python.framework/Versions/3.12/bin
    - User: /Users/zach/Library/Python/3.12/bin
    - prefix: /opt/homebrew/bin

    Returns
    -------
    Tuple[ScriptPathHome, ScriptPathUser, ScriptPathPrefix]
        Tuple of script path strings for User, Home, and Prefix strings
    """

    script_paths = []
    scheme_keys = ["home", "user", "prefix"]
    # scheme_keys: List[Literal["user", "home", "prefix"]] = ["user", "home", "prefix"]
    for key in scheme_keys:
        scheme = sysconfig.get_preferred_scheme(key)  # type: ignore
        script_path = sysconfig.get_path("scripts", scheme)
        script_paths.append(script_path)

    return tuple(script_paths)
