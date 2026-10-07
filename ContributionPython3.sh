#!/bin/bash

# Runs the Melissa Contribution Cloud API Python 3 sample.
#
# This script runs ContributionPython3.py with python3, passing along the license and
# (if supplied) the contribution fields.
#
# Overall flow:
#   1. Parse the command-line options below.
#   2. Resolve the license (--license, then a prompt, then the MD_LICENSE environment variable).
#   3. Run ContributionPython3.py: with the contribution fields if any was supplied,
#      otherwise with only the license (the Python program prompts for each field).
#
# Options (each takes a value):
#   --lat         Proposed latitude for the address.
#   --long        Proposed longitude for the address.
#   --mak         Melissa Address Key (MAK) of the address to correct.
#   --reason      Reason for the change.
#   --respondTo   Contact (e.g. an email address) to respond to about the contribution.
#   --license     License string. If omitted, the script prompts for it; if the prompt
#                 is left blank, it falls back to MD_LICENSE. Running without --license
#                 always prompts, even when MD_LICENSE is set.
#
# Examples:
#   ./ContributionPython3.sh --license "your-license"
#   ./ContributionPython3.sh --lat "33.637562" --long "-117.606887" --mak "8008006245" --reason "GeoPoint Change needed" --respondTo "youremail@melissadata.com" --license "your-license"

######################### Constants ##########################

RED='\033[0;31m' #RED
NC='\033[0m' # No Color

######################### Parameters ##########################

lat=""
long=""
mak=""
reason=""
respondTo=""
license=""

# Read each --flag and its value. A flag with no value, or whose value looks like an
# option name (e.g. --lat), is an error; other values starting with "-", such as
# negative coordinates, are allowed. Unrecognized options are ignored.
while [ $# -gt 0 ] ; do
  case $1 in
    --lat)
        if [ -z "$2" ] || [[ $2 =~ ^--?[a-zA-Z]+$ ]];
        then
            printf "${RED}Error: Missing an argument for parameter 'lat'.${NC}\n"
            exit 1
        fi
        lat="$2"
        shift
        ;;
    --long)
        if [ -z "$2" ] || [[ $2 =~ ^--?[a-zA-Z]+$ ]];
        then
            printf "${RED}Error: Missing an argument for parameter 'long'.${NC}\n"
            exit 1
        fi
        long="$2"
        shift
        ;;
    --mak)
        if [ -z "$2" ] || [[ $2 =~ ^--?[a-zA-Z]+$ ]];
        then
            printf "${RED}Error: Missing an argument for parameter 'mak'.${NC}\n"
            exit 1
        fi
        mak="$2"
        shift
        ;;
    --reason)
        if [ -z "$2" ] || [[ $2 =~ ^--?[a-zA-Z]+$ ]];
        then
            printf "${RED}Error: Missing an argument for parameter 'reason'.${NC}\n"
            exit 1
        fi
        reason="$2"
        shift
        ;;
    --respondTo)
        if [ -z "$2" ] || [[ $2 =~ ^--?[a-zA-Z]+$ ]];
        then
            printf "${RED}Error: Missing an argument for parameter 'respondTo'.${NC}\n"
            exit 1
        fi
        respondTo="$2"
        shift
        ;;
    --license)
        if [ -z "$2" ] || [[ $2 =~ ^--?[a-zA-Z]+$ ]];
        then
            printf "${RED}Error: Missing an argument for parameter 'license'.${NC}\n"
            exit 1
        fi
        license="$2"
        shift
        ;;
  esac
  shift
done

########################## Main ############################
printf "\n======================= Melissa Contribution Cloud API =========================\n"

# Get license (either from parameters or user input)
if [ -z "$license" ];
then
  printf "Please enter your license string: "
  read license
fi

# Check for License from Environment Variables 
if [ -z "$license" ];
then
  license=`echo $MD_LICENSE` 
fi

if [ -z "$license" ];
then
  printf "\nLicense String is invalid!\n"
  exit 1
fi

# Run project
# No contribution fields supplied -> run with only the license (the program prompts for each field);
# otherwise pass them all through. Unsupplied fields arrive as empty strings, and the
# program prompts for them.
if [ -z "$lat" ] && [ -z "$long" ] && [ -z "$mak" ] && [ -z "$reason" ] && [ -z "$respondTo" ];
then
    python3 ContributionPython3.py --license "$license"
else
    python3 ContributionPython3.py --license "$license" --lat "$lat" --long "$long" --mak "$mak" --reason "$reason" --respondTo "$respondTo"
fi

