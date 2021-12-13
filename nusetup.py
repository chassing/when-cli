from nudev.api.v4 import PackageBattery, ProjectConfigBase, PythonBattery, SourceConfigBase


class SourceConfig(PythonBattery, PackageBattery, SourceConfigBase):
    """Source config for when-cli."""

    name = "when-cli"
    version = "0.1"


class ProjectConfig(ProjectConfigBase):
    """Project config for when-cli."""

    name = "when-cli"
    sources = [SourceConfig]


project = ProjectConfig()
