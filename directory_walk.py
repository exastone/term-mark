import os
from datetime import datetime


def find_git_directories(func):
    def wrapper(*args, **kwargs):
        paths_to_search = func(*args, **kwargs)
        git_dirs = []

        for path in paths_to_search:
            for root, dirs, files in os.walk(path):
                if '.git' in dirs:
                    git_dirs.append(os.path.join(root, '.git'))

        return git_dirs

    return wrapper


def walk_top_level_directory(path):
    absolute_path = os.path.abspath(path)

    if not os.path.exists(absolute_path):
        print(f"The provided path '{path}' does not exist.")
        return []

    return [absolute_path]


@find_git_directories
def walk_subdirectories(paths, include_files=False, search_depth=None):
    results = []

    for path in paths:
        for root, dirs, files in os.walk(path):
            relative_root = os.path.relpath(root, path)

            # Calculate the depth of the current directory
            current_depth = len(relative_root.split(os.path.sep))

            # Check if the current depth is within the specified max_depth
            if search_depth is None or current_depth <= search_depth:
                results.append(os.path.join(path, relative_root))

                if include_files:
                    for file in files:
                        results.append(os.path.join(path, relative_root, file))

    return results


def contains_item(directory, name):
    return name in os.listdir(directory)


def get_subdirectories(path, max_results=None, include_hidden=False, max_search_depth=None) -> list[str]:
    subdirectories = []
    stack = [(os.path.abspath(path), 0)]  # Using a stack to simulate recursion

    while stack:
        current_path, current_depth = stack.pop()

        if max_search_depth is not None and current_depth > max_search_depth:
            continue

        for item in sorted(os.listdir(current_path), key=str.lower):
            item_path = os.path.join(current_path, item)
            if os.path.isdir(item_path):
                if not include_hidden and item.startswith('.'):
                    continue
                subdirectories.append(item_path)
                if len(subdirectories) >= max_results:
                    return subdirectories
                stack.append((item_path, current_depth + 1))

    return subdirectories


# return atime as unix epoch int
def get_last_access_time(path) -> int:
    access_time = int(os.path.getatime(path))
    return access_time


# return mtime as unix epoch int
def get_last_modification_time(path) -> int:
    mod_time = int(os.path.getmtime(path))
    return mod_time


def unix_timestamp_to_datetime(unix_timestamp):
    datetime_obj = datetime.fromtimestamp(unix_timestamp)
    datetime_info = {
        "year": datetime_obj.year,
        "month": datetime_obj.month,
        "day": datetime_obj.day,
        "hour": datetime_obj.hour,
        "minute": datetime_obj.minute,
        "second": datetime_obj.second,
        "weekday": datetime_obj.strftime('%a'),  # Full weekday name
        "month_name": datetime_obj.strftime('%b')  # Full month name
    }
    return datetime_info
