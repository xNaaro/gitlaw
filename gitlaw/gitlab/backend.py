"""Module to orchestrate gitlab interactions."""
import gitlab

from gitlaw.gitlab.settings import Settings
from gitlaw.gitlab.groups import Groups

class GitlabBackend:
    """Gitlab class.

    Manages interactions with GitLab APIs.
    """
    def __init__(self, config, server_url, server_auth_token) -> None:
        """Init class.
        
        Args:
        config: Config data.
        server_url: GitLab server URL.
        server_auth_token: Gitlab auth token

        Returns: None
        """
        self.config = config
        self.gl = self.handle_auth(server_url, server_auth_token)

    def entrypoint(self) -> None:
        """Call gitlab methods."""
        print("Configuring service...")
        Settings(self.gl, self.config.get('service')).manager()
        for group in self.config.get('groups'):
            Groups(self.gl, group).manager(configure_groups=self.config.get('configure_groups', True),
                                           configure_projects=self.config.get('configure_projects', True),
                                           auto_create_groups=self.config.get('auto_create_groups', True))

    def handle_auth(self, server_url, server_auth_token) -> object:
        """Init gitlab object with auth.

        Args:
        server_url: GitLab server URL.
        server_auth_token: Gitlab auth token
        ssl_verify: Verify SSL connections, defaults to False
        """
        gl = gitlab.Gitlab(url=server_url, private_token=server_auth_token, ssl_verify=False)
        return gl
