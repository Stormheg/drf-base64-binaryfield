#!/bin/sh

# This script is used to compile translations
# Usage:
#
# ./compile_translations.sh

set -e

cd src && django-admin compilemessages $@
