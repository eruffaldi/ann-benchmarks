#!/bin/bash
#
# docker run 
git clone --depth 1 https://github.com/eruffaldi/half.git
cd half
mkdir build
cd build
export CXXFLAGS=-march=native
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_POSITION_INDEPENDENT_CODE=ON ..
make -j
make install
