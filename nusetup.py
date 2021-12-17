from nudev.api.v4 import PackageBattery, ProjectConfigBase, PublishOptMixin, PythonBinaryBattery, SourceConfigBase


class SourceConfig(PythonBinaryBattery, PublishOptMixin, PackageBattery, SourceConfigBase):
    """Source config for when-cli."""

    name = "when-cli"
    version = "1.0"
    script_names = ["when/when/__main__.py"]
    python = python_shebang = python_interpreter = "/usr/bin/python3.8"


class ProjectConfig(ProjectConfigBase):
    """Project config for when-cli."""

    name = "when-cli"
    sources = [SourceConfig]


project = ProjectConfig()
