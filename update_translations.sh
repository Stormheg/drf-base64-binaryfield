#!/bin/sh

# This script is used to update and manage translations.
# Usage:
#
# Update all languages:
# ./update_translations.sh --all
#
# Create new language:
# ./update_translations.sh -l <language_code>

set -e

cd src && python ../manage.py makemessages $@
