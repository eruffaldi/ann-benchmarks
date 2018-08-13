#!/bin/bash
#
# docker run 
git clone --depth 1 https://github.com/eruffaldi/berkeley-softfloat-3.git
cd berkeley-softfloat-3
mkdir build
cd build
export CXXFLAGS=-march=native
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_POSITION_INDEPENDENT_CODE=ON ..
make -j
make install
