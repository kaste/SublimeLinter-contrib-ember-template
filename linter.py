# Linter for SublimeLinter, a code checking framework for Sublime Text
#
# Written by raphaelns-developer and kaste
# Copyright (c) 2018 raphaelns
# Copyright (c) 2022 kaste
#
# License: MIT
#

"""This module exports the Ember Template Linter plugin class."""
from itertools import chain
import json
import re

from SublimeLinter.lint import LintMatch, NodeLinter

flatten = chain.from_iterable


class EmberTemplateLint(NodeLinter):
    """Provides an interface to the ember template linter executable."""
    name = 'ember-template'
    cmd = 'ember-template-lint --format=json $args -'

    missing_config_regex = re.compile(
        r'^(.*?)\r?\n\w*(Ember template linter couldn\'t find a configuration file.)',
        re.DOTALL
    )
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

    """
      {
        "D:\\tember-template-linter\\test.hbs": [
          {
            "rule": "no-bare-strings",
            "severity": 2,
            "filePath": "D:\\tember-template-linter\\test.hbs",
            "line": 2,
            "column": 5,
            "endLine": 2,
            "endColumn": 18,
            "source": "A bare string",
            "message": "Non-translated string used"
          }
        ]
      }
    """

    def find_errors(self, output):
        """Parse errors from linter's output."""
        if not output.strip():
            return

        try:
            content = json.loads(output)
        except ValueError:
            self.logger.error(
                "JSON Decode error: We expected JSON from 'ember-template-lint', "
                "but instead got this:\n{}\n\n"
                .format(output))
            self.notify_failure()
            return

        for fact in flatten(content.values()):
            severity = "error" if fact["severity"] == 2 else "warning"
            yield LintMatch(
                match=fact,
                filename   = fact["filePath"],      # noqa: E221, E251
                message    = fact["message"],       # noqa: E221, E251
                line       = fact["line"] - 1,      # noqa: E221, E251
                col        = fact["column"],        # noqa: E221, E251
                end_line   = fact["endLine"] - 1,   # noqa: E221, E251
                end_col    = fact["endColumn"],     # noqa: E221, E251
                error_type = severity,              # noqa: E251
                code       = fact.get("rule", ""),  # noqa: E221, E251
            )
