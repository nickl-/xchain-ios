CFLAGS = -m32 -fno-builtin-round -fno-builtin-trunc
CPPFLAGS = 
DEFS = -DHAVE_CONFIG_H
LDFLAGS = -m32

builddir = .
abs_builddir = /home/JC/ios/xchain-ios/cctools-806
top_builddir = .
abs_top_builddir = /home/JC/ios/xchain-ios/cctools-806
srcdir = .
abs_srcdir = /home/JC/ios/xchain-ios/cctools-806
top_srcdir = .
abs_top_srcdir = /home/JC/ios/xchain-ios/cctools-806



COMPONENTS = ar as include libstuff libmacho ld man misc otool

.PHONY: default install clean distclean $(COMPONENTS)

default: $(COMPONENTS)

$(COMPONENTS):
	cd $@ && $(MAKE)

as ar ld ld64 misc otool: libstuff

clean distclean install:
	for c in $(COMPONENTS); do              	\
		(cd $$c && $(MAKE) $@) || exit 1;	\
	done

$(srcdir)/configure: configure.ac
	cd $(srcdir) && autoconf

$(srcdir)/include/config.h.in: include/stamp-h.in
$(srcdir)/include/stamp-h.in: configure.ac
	cd $(srcdir) && autoheader
	echo timestamp > $(srcdir)/include/stamp-h.in

include/config.h: include/stamp-h
include/stamp-h: include/config.h.in config.status
	./config.status

Makefile: Makefile.in config.status
	./config.status

config.status: configure
	./config.status --recheck

