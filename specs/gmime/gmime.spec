# $Id$
# Authority: dag

Summary: Library for creating and parsing MIME messages
Name: gmime
Version: 2.5.3
Release: 1%{?dist}
License: GPL
Group: System Environment/Libraries
URL: http://spruce.sourceforge.net/gmime/

Source: http://ftp.acc.umu.se/pub/GNOME/sources/gmime/2.5/gmime-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: glib2-devel >= 2.12
BuildRequires: zlib-devel >= 1.2.1.1

%description
The GMime suite provides a core library and set of utilities which may be
used for the creation and parsing of messages using the Multipurpose
Internet Mail Extension (MIME).

%package devel
Summary: Header files, libraries and development documentation for %{name}.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: glib2-devel

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup

%build
%configure --disable-static
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"

%{__mv} -v %{buildroot}%{_bindir}/uuencode %{buildroot}%{_bindir}/gmime-uuencode
%{__mv} -v %{buildroot}%{_bindir}/uudecode %{buildroot}%{_bindir}/gmime-uudecode

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING README TODO
%{_bindir}/gmime-uudecode
%{_bindir}/gmime-uuencode
%{_libdir}/libgmime-2.6.so.*

%files devel
%defattr(-, root, root, 0755)
%doc %{_datadir}/gtk-doc/html/gmime-2.5/
#%{_bindir}/gmime-config
%{_includedir}/gmime-2.6/
%{_libdir}/libgmime-2.6.so
%{_libdir}/pkgconfig/gmime-2.6.pc
%exclude %{_libdir}/libgmime-2.6.la

%changelog
* Sun Nov 21 2010 Dag Wieers <dag@wieers.com> - 2.5.3-1
- Updated to release 2.5.3.

* Wed Mar 21 2007 Dag Wieers <dag@wieers.com> - 2.2.4-1
- Initial package. (using DAR)
