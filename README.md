SublimeLinter-contrib-ember-template-linter
================================
[![tests](https://github.com/kaste/SublimeLinter-contrib-ember-template/actions/workflows/ci.yml/badge.svg)](https://github.com/kaste/SublimeLinter-contrib-ember-template/actions/workflows/ci.yml)


This linter plugin for [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter) provides an interface to [ember-template-linter](https://github.com/ember-template-lint/ember-template-lint). It will be used with files that have the “handlebars” syntax.

## Installation
SublimeLinter must be installed in order to use this plugin. 

Please use [Package Control](https://packagecontrol.io) to install the linter plugin.

Before using this plugin, ensure that `ember-template-linter` is installed on your system.
To install `ember-template-linter`, do the following:

- Install [Node.js](http://nodejs.org) (and [npm](https://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager) on Linux).

- Install `ember-template-linter` globally by typing the following in a terminal:
```
npm install -g ember-template-linter
```
    
- Or install `ember-template-linter` locally in your project folder (**you must have package.json file there**):
```
npm install ember-template-linter
```


In order for `ember-template-linter` to be executed by SublimeLinter, you must ensure that its path is available to SublimeLinter. The docs cover [troubleshooting PATH configuration](http://sublimelinter.readthedocs.io/en/latest/troubleshooting.html#finding-a-linter-executable).

## Settings
- SublimeLinter settings: http://sublimelinter.readthedocs.org/en/latest/settings.html
- Linter settings: http://sublimelinter.readthedocs.org/en/latest/linter_settings.html
