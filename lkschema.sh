# Bash script to run converter from command line

ERROR="No filename specified. Please specify a filename to convert (e.g., resource/schema.txt)."
INVALID_PATH="Specified path does not exist."

if [ -z $1 ]; then
    echo $ERROR
elif [ ! -d "$1" ]; then
    echo $INVALID_PATH
fi

DIRNAME=$(dirname $1)
BASENAME=$(basename $1)
OUTPUT=$BASENAME.json

if [ -n $2 ]; then
    OUTPUT=$2
fi

echo Converting $1 to $OUTPUT
# python -m main -f %1 -o %2
