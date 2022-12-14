SublimeLinter-contrib-ember-template
====================================

[![tests](https://github.com/kaste/SublimeLinter-contrib-ember-template/actions/workflows/ci.yml/badge.svg)](https://github.com/kaste/SublimeLinter-contrib-ember-template/actions/workflows/ci.yml)


This linter plugin for [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter) provides an interface to [ember-template-lint](https://github.com/ember-template-lint/ember-template-lint). It will be used with files that have the “handlebars” syntax.

## Installation
SublimeLinter must be installed in order to use this plugin. 

Please use [Package Control](https://packagecontrol.io) to install the linter plugin.

Before using this plugin, ensure that `ember-template-lint` is installed on your system.
To install `ember-template-lint`, usually do the following:

```
npm install --save-dev ember-template-lint
```

But newer ember apps have it preinstalled.

Note that `ember-template-lint` *requires* a configuration file but does *not*
error if it can't find any!  (So it can look like you're green and everything
is okay to commit when in fact it didn't do anything.)
