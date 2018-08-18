#!/bin/bash
#
# docker run 
git clone --depth 1 https://gitlab.com/cerlane/SoftPosit
cd SoftPosit
#!/bin/bash
sed 's/double toDouble\(\)/\
	explicit operator double() const { return toDouble(); }\
	explicit operator float() const { return toDouble(); }\
	&/' source/include/softposit_cpp.h > tmp
cp tmp source/include/softposit_cpp.h
cd build/Linux-x86_64-GCC
make	
cp softposit.a /usr/lib/libsoftposit.a
cp ../../source/include/softposit.h ../../source/include/softposit_cpp.h ../../source/include/softposit_types.h /usr/include