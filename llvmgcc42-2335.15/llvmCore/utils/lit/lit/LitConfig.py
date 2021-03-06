class LitConfig:
    """LitConfig - Configuration data for a 'lit' test runner instance, shared
    across all tests.

    The LitConfig object is also used to communicate with client configuration
    files, it is always passed in as the global variable 'lit' so that
    configuration files can access common functionality and internal components
    easily.
    """

    # Provide access to built-in formats.
    import LitFormats as formats

    # Provide access to built-in utility functions.
    import Util as util

    def __init__(self, progname, path, quiet,
                 useValgrind, valgrindArgs,
                 useTclAsSh,
                 noExecute, debug, isWindows,
                 params):
        # The name of the test runner.
        self.progname = progname
        # The items to add to the PATH environment variable.
        self.path = list(map(str, path))
        self.quiet = bool(quiet)
        self.useValgrind = bool(useValgrind)
        self.valgrindArgs = list(valgrindArgs)
        self.useTclAsSh = bool(useTclAsSh)
        self.noExecute = noExecute
        self.debug = debug
        self.isWindows = bool(isWindows)
        self.params = dict(params)
        self.bashPath = None

        self.numErrors = 0
        self.numWarnings = 0

    def load_config(self, config, path):
        """load_config(config, path) - Load a config object from an alternate
        path."""
        from TestingConfig import TestingConfig
        return TestingConfig.frompath(path, config.parent, self,
                                      mustExist = True,
                                      config = config)

    def getBashPath(self):
        """getBashPath - Get the path to 'bash'"""
        import os, Util

        if self.bashPath is not None:
            return self.bashPath

        self.bashPath = Util.which('bash', os.pathsep.join(self.path))
        if self.bashPath is None:
            # Check some known paths.
            for path in ('/bin/bash', '/usr/bin/bash'):
                if os.path.exists(path):
                    self.bashPath = path
                    break

        if self.bashPath is None:
            self.warning("Unable to find 'bash', running Tcl tests internally.")
            self.bashPath = ''

        return self.bashPath

    def _write_message(self, kind, message):
        import inspect, os, sys

        # Get the file/line where this message was generated.
        f = inspect.currentframe()
        # Step out of _write_message, and then out of wrapper.
        f = f.f_back.f_back
        file,line,_,_,_ = inspect.getframeinfo(f)
        location = '%s:%d' % (os.path.basename(file), line)

        print >>sys.stderr, '%s: %s: %s: %s' % (self.progname, location,
                                                kind, message)

    def note(self, message):
        self._write_message('note', message)

    def warning(self, message):
        self._write_message('warning', message)
        self.numWarnings += 1

    def error(self, message):
        self._write_message('error', message)
        self.numErrors += 1

    def fatal(self, message):
        import sys
        self._write_message('fatal', message)
        sys.exit(2)
