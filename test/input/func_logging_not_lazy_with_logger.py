"""Logging warnings using a logger class."""
from __future__ import absolute_import
__revision__ = ''

import logging


LOG = logging.getLogger("domain")
LOG.debug("%s" % "junk")
LOG.log(logging.DEBUG, "%s" % "junk")
LOG2 = LOG.debug
LOG2("%s" % "junk")

logging.getLogger("domain").debug("%s" % "junk")
