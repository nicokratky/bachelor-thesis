#!/bin/sh
# Copyright (C) 2014-2023 by Thomas Auzinger <thomas@auzinger.name>

CLASS=vutinfth
SOURCE=thesis

# Build vutinfth documentation
latexmk $CLASS.dtx

# Build the vutinfth class file
latexmk $CLASS.ins

# Build the thesis document
latexmk -pdf $SOURCE

echo
echo
echo Class file and document compiled.
