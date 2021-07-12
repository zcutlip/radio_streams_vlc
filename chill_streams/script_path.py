from setuptools import Distribution
from setuptools.command.install import install


class OnlyGetScriptPath(install):

    def finalize_options(self):
        if self.distribution.user:
            self.user = self.distribution.user
            self.prefix = None
        super().finalize_options()

    def run(self):
        # does not call install.run() by design
        self.distribution.install_scripts = self.install_scripts


def get_setuptools_script_dir(user=False):
    dist = Distribution({'cmdclass': {'install': OnlyGetScriptPath}})
    dist.dry_run = True  # not sure if necessary, but to be safe
    if user:
        dist.user = True
    else:
        dist.user = False
    dist.parse_config_files()
    # install_opts["user"] = True
    # install_opts["prefix"] = ""
    command = dist.get_command_obj('install')
    command.ensure_finalized()
    command.run()
    return dist.install_scripts
