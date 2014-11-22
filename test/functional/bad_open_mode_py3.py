"""Warnings for using open() with an invalid mode string."""

NAME = "foo.bar"
open(NAME, "wb")
open(NAME, "w")
open(NAME, "rb")
open(NAME, "x")
open(NAME, "br")
open(NAME, "+r")
open(NAME, "xb")
open(NAME, "rwx")  # [bad-open-mode]
open(NAME, "rr")  # [bad-open-mode]
open(NAME, "+")  # [bad-open-mode]
