
#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by roadhump
# Copyright (c) 2014 roadhump
#
# License: MIT
#

"""This module exports the Ember Template Linter plugin class."""
import json
import logging
import os
import re
from SublimeLinter.lint import NodeLinter 

logger = logging.getLogger('SublimeLinter.plugin.embertemplatelint')

class EmberTemplateLint(NodeLinter):
    """Provides an interface to the ember template linter executable."""

    npm_name = 'embertemplatelint'
    cmd = 'ember-template-lint ${file} --json'

    missing_config_regex = re.compile(
        r'^(.*?)\r?\n\w*(Ember template linter couldn\'t find a configuration file.)',
        re.DOTALL
    )
    line_col_base = (1, 1)
    defaults = {
        'selector': 'text.html.handlebars'
    }

    def on_stderr(self, stderr):
        # Demote 'annoying' config is missing error to a warning.
        if self.missing_config_regex.match(stderr):
            logger.warning(stderr)
            self.notify_failure()
        elif (
            'DeprecationWarning' in stderr or
            'ExperimentalWarning' in stderr or
            'in the next version' in stderr  # is that a proper deprecation?
        ):
            logger.warning(stderr)
        else:
            logger.error(stderr)
            self.notify_failure()

    def find_errors(self, output):
        """Parse errors from linter's output."""
        try:
            content = json.loads(output)
        except ValueError:
            logger.error(
                "JSON Decode error: We expected JSON from 'ember-template-lint', "
                "but instead got this:\n{}\n\n"
                "output.".format(output))
            self.notify_failure()
            return

        if logger.isEnabledFor(logging.INFO):
            import pprint
            logger.info(
                '{} output:\n{}'.format(self.name, pprint.pformat(content)))

        for match in content[self.filename]:
                if match['message'].startswith('File ignored'):
                    continue

                column = match.get('column', None)
                ruleId = match.get('rule', '')

                yield (
                    match,
                    match['line'] - 1,  # apply line_col_base manually
                    column,
                    ruleId if match['severity'] == 2 else '',
                    ruleId if match['severity'] == 1 else '',
                    match['message'],
                    None  # near
                )

    def reposition_match(self, line, col, m, vv):
        match = m.match
        if (
            col is None or
            'endLine' not in match or
            'endColumn' not in match
        ):
            return super().reposition_match(line, col, m, vv)

        # apply line_base manually
        end_line = match['endLine'] - 1
        end_column = match['endColumn']

        for _line in range(line, end_line):
            text = vv.select_line(_line)
            end_column += len(text)

        return line, col, end_column

    def run(self, cmd, code):
        return super().run(cmd, code)
