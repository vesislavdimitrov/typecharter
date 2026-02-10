#!/bin/bash

echo "Building TypeCharter executable..."

rm -rf build/
rm -rf dist/
rm -f ./*.spec

pyinstaller --onedir \
    --windowed \
    --name "TypeCharter" \
    --add-data "lib:lib" \
    --hidden-import pandas \
    --hidden-import matplotlib.backends.backend_tkagg \
    --hidden-import matplotlib.backends._backend_tk \
    --hidden-import matplotlib.backends.backend_agg \
    --exclude-module scipy \
    --exclude-module sklearn \
    --exclude-module seaborn \
    --exclude-module IPython \
    --exclude-module jupyter \
    --exclude-module matplotlib.tests \
    --exclude-module numpy.tests \
    --exclude-module pandas.tests \
    --strip \
    --optimize=2 \
    typecharter.py

echo "DONE."