##########################################################################################
""" that one is too long tooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"""

__revision__ = ''

# The next line is exactly 80 characters long.
A = '--------------------------------------------------------------------------'

# The next line is longer than 80 characters, because the file is encoded
# in ASCII.
THIS_IS_A_VERY_LONG_VARIABLE_NAME = 'Существительное Частица'  # With warnings.

# Do not trigger the line-too-long warning if the only token that makes the
# line longer than 80 characters is a trailing pylint disable.
var = 'This line has a disable pragma and whitespace trailing beyond 80 chars. '  # pylint:disable=invalid-name

badname = 'This line is already longer than 80 characters even without the pragma.'  # pylint:disable=invalid-name

# http://example.com/this/is/a/very/long/url?but=splitting&urls=is&a=pain&so=they&can=be&long
