#!/bin/bash
#
# docker run 
git clone --depth 1 https://github.com/stillwater-sc/universal
cd universal
mkdir build
cd build
cmake -DBUILD_APPLICATION_EXAMPLES=OFF -DCMAKE_CXX_FLAGS=-march=native -DBUILD_EDUCATION_EXAMPLES=OFF -DBUILD_PLAYGROUND=OFF -DBUILD_UNUM_TYPE_3_POSIT=ON  ..
make
#define POSIT_THROW_ARITHMETIC_EXCEPTION 1
cd ..
mkdir /usr/include/stillwater
cp -r bitblock posit /usr/include/stillwater
