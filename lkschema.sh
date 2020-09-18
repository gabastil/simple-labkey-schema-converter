# Bash script to run converter from command line

ERROR="No filename specified. Please specify a filename to convert (e.g., resource/schema.txt)."
INVALID_PATH="Specified path does not exist."
SUCCESS="Converting $1 to "

if [ "$1" = "" ]; then
    echo $ERROR;
elif [ ! -d "$1" ]; then
    echo "$INVALID_PATH"
fi

# python -m main -f %1
