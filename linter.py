# Linter for SublimeLinter, a code checking framework for Sublime Text
#
# Written by raphaelns-developer and kaste
# Copyright (c) 2018 raphaelns
# Copyright (c) 2022 kaste
#
# License: MIT
#

"""This module exports the Ember Template Linter plugin class."""
import re
from SublimeLinter.lint import NodeLinter 


class EmberTemplateLint(NodeLinter):
    """Provides an interface to the ember template linter executable."""
    name = 'ember-template'
    cmd = 'ember-template-lint -'

    missing_config_regex = re.compile(
        r'^(.*?)\r?\n\w*(Ember template linter couldn\'t find a configuration file.)',
        re.DOTALL
    )
    regex = (
        r'.+?'
        r'(?P<line>\d+):(?P<col>\d+)'
        r'\s+(?P<error_type>\S+)\s+'
        r'(?P<message>.*)'
        r'\s+'
        r'(?P<code>.*)'
    )
    line_col_base = (1, 0)
    defaults = {
        'selector': 'text.html.handlebars',
        '--filename': '${file}',
    }

    def on_stderr(self, stderr):
        # Demote 'annoying' config is missing error to a warning.
        if self.missing_config_regex.match(stderr):
            self.logger.warning(stderr)
            self.notify_failure()
        elif (
            'DeprecationWarning' in stderr or
            'ExperimentalWarning' in stderr or
            'in the next version' in stderr  # is that a proper deprecation?
        ):
            self.logger.warning(stderr)
        else:
            self.logger.error(stderr)
            self.notify_failure()
