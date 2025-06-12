#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

pip3 install conan

PROJECT_FOLDER="EIPScanner"


mkdir -p "${SCRIPT_DIR}/build"
cd "${SCRIPT_DIR}/build"

conan install .. --build=missing -s build_type=Release

cmake "${SCRIPT_DIR}/${PROJECT_FOLDER}" \
    -DCMAKE_BUILD_TYPE=Release \
    -G "Unix Makefiles" \
    -DCMAKE_TOOLCHAIN_FILE="${SCRIPT_DIR}/conan_toolchain.cmake"
cmake --build . --config Release
if [ $? -ne 0 ]; then
    echo "Build failed. Please check the output for errors."
    exit 1
fi
echo "Build completed successfully."

cmake --install . --config Release
