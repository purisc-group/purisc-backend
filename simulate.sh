#!/bin/sh

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <filename>" >&2
    exit 1
fi

filename="${1%.*}";

clang-3.5 -S -emit-llvm $1
python "${PURISC_PATH}/jab/compiler.py" -i "${filename}.ll" -o "${filename}.subleq"
python "${PURISC_PATH}/assembler/assembler.py" -i "${filename}.subleq" -o "${filename}.machine"
python "${PURISC_PATH}/simulator/sim.py" -i "${filename}.machine"