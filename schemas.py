class Project:
    def __init__(self, id, project_name, project_path, atime, mtime, is_git):
        self.id = id
        self.project_name = project_name
        self.project_path = project_path
        self.atime = atime
        self.mtime = mtime
        self.is_git = is_git

    def __str__(self):
        return f"{self.project_name}: {self.project_path}"
