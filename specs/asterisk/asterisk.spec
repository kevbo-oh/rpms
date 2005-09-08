# $Id$
# Authority: matthias

# The user and group names
%define uname asterisk
%define gname asterisk

# For pre or post versions
#define prever RC2
#define cvs 20041125

Summary: PBX and telephony application and toolkit
Name: asterisk
Version: 1.0.9
Release: %{?prever:0.%{prever}.}%{?cvs:1.%{cvs}.}1
License: GPL
Group: Applications/Internet
URL: http://www.asterisk.org/
Source0: ftp://ftp.digium.com/pub/asterisk/asterisk-%{version}%{?prever:-%{prever}}.tar.gz
Source1: asterisk.init
Patch0: asterisk-1.0-RC2-cdr.patch
Patch1: get-data-char-escape.patch2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: perl, zaptel
BuildRequires: openssl-devel, zlib-devel, perl, bison, speex-devel, zaptel
BuildRequires: gtk+-devel, newt-devel, ncurses-devel, doxygen
%{!?_without_mysql:BuildRequires: mysql-devel}
%{!?_without_postgresql:BuildRequires: postgresql-devel}
%{!?_without_sqlite:BuildRequires: sqlite-devel}

%description
Asterisk is an Open Source PBX and telephony development platform that
can both replace a conventional PBX and act as a platform for developing
custom telephony applications for delivering dynamic content over a
telephone similarly to how one can deliver dynamic content through a
web browser using CGI and a web server.
 
Asterisk talks to a variety of telephony hardware including BRI, PRI,
POTS, and IP telephony clients using the Inter-Asterisk eXchange
protocol (e.g. gnophone or miniphone).


%package devel
Summary: Header files and development documentation for Asterisk
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
This package contains the header files needed to compile modules for Asterisk
as well as the developer documentation generated by doxygen.


%prep
%setup -n asterisk-%{version}%{?prever:-%{prever}}
%patch0 -p1 -b .cdr
%patch1 -p0 -b .datacharescape
# Replace /var/run by /var/run/asterisk since we don't run as root
%{__perl} -pi.orig -e 's|/var/run$|%{_var}/run/asterisk|g' Makefile
# Fix lib vs. lib64 directory
%{__perl} -pi -e 's|/usr/lib/asterisk$|%{_libdir}/asterisk|g' Makefile


%build
%{__make} PROC="%{_arch}" OPTIMIZE="%{optflags}" 
%{__make} progdocs


%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}
# Install all sample config files
%{__make} samples DESTDIR=%{buildroot}
%{__install} -Dp -m0755 %{SOURCE1} \
    %{buildroot}%{_sysconfdir}/rc.d/init.d/asterisk

# We need that directory, see above
%{__mkdir_p} %{buildroot}%{_var}/run/asterisk

# Fix the safe_asterix script, to be run as non-root
%{__perl} -pi -e 's|(asterisk \${CLIARGS})|%{_sbindir}/$1|g' \
    %{buildroot}%{_sbindir}/safe_asterisk

# Install demo sounds
for file in sounds/demo-*; do
    %{__install} -p -m0644 $file %{buildroot}%{_var}/lib/asterisk/sounds/
done
for file in sounds/*.mp3; do
    %{__install} -p -m0644 $file %{buildroot}%{_var}/lib/asterisk/mohmp3/
done


%clean
%{__rm} -rf %{buildroot}


%pre
# Add the "asterisk" user
/usr/sbin/useradd -c "Asterisk PBX" -G tty -s /sbin/nologin -r \
    -d "%{_var}/lib/asterisk" %{uname} 2>/dev/null || :

%post
# Register the asterisk service
/sbin/chkconfig --add asterisk
# Fix the permission on tty9
/bin/chmod g+r /dev/tty9

%preun
if [ $1 -eq 0 ]; then
    /sbin/service asterisk stop >/dev/null 2>&1
    /sbin/chkconfig --del asterisk
fi


%files
%defattr(-, root, root, 0755)
%doc BUGS ChangeLog CREDITS HARDWARE LICENSE README SECURITY doc/*.txt configs/
%doc sounds.txt
%attr(750, %{uname}, %{gname}) %dir %{_sysconfdir}/asterisk
%attr(640, %{uname}, %{gname}) %config(noreplace) %{_sysconfdir}/asterisk/*.conf
%attr(640, %{uname}, %{gname}) %config(noreplace) %{_sysconfdir}/asterisk/*.adsi
%{_sysconfdir}/rc.d/init.d/asterisk
%{_libdir}/asterisk/
%{_sbindir}/*
%{_mandir}/man8/asterisk.8*
%attr(-  , %{uname}, %{gname}) %{_var}/lib/asterisk/
%attr(750, %{uname}, %{gname}) %{_var}/run/asterisk/
%attr(750, %{uname}, %{gname}) %dir %{_var}/log/asterisk/
%attr(750, %{uname}, %{gname}) %dir %{_var}/spool/asterisk/
                                    %{_var}/spool/asterisk/vm/
%attr(750, %{uname}, %{gname}) %dir %{_var}/spool/asterisk/voicemail/
%attr(750, %{uname}, %{gname}) %dir %{_var}/spool/asterisk/voicemail/default/
%attr(750, %{uname}, %{gname}) %dir %{_var}/spool/asterisk/voicemail/default/1234/
                                    %{_var}/spool/asterisk/voicemail/default/1234/*.gsm


%files devel
%defattr(-, root, root, 0755)
%doc doc/api/html/*
%{_includedir}/asterisk/


%changelog
* Tue Aug 23 2005 Matthias Saou <http://freshrpms.net> 1.0.9-1
- Update to 1.0.9.
- Change ASTLIBDIR to fix lib64 file location issue.

* Tue Apr  5 2005 Matthias Saou <http://freshrpms.net> 1.0.7-1
- Update to 1.0.7.

* Tue Mar  8 2005 Matthias Saou <http://freshrpms.net> 1.0.6-1
- Update to 1.0.6.

* Wed Feb  2 2005 Matthias Saou <http://freshrpms.net> 1.0.5-1
- Update to 1.0.5.
- Don't create nor include sbin/safe_asterisk.orig.
- Remove now unneeded absolute symlink overriding (they point inside now).
- Replace localstatedir by var for mdk compat and initrddir by full path.

* Fri Nov 26 2004 Matthias Saou <http://freshrpms.net> 1.0.2-1.20041125.0
- Update to CVS snapshot.

* Mon Oct 18 2004 Matthias Saou <http://freshrpms.net> 1.0.1-0
- Update to 1.0.1.

* Wed Sep  1 2004 Matthias Saou <http://freshrpms.net> 1.0-0.RC2.1
- Fix safe_asterisk again, ${CLIARGS} instead of ${ASTARGS}.

* Thu Aug 26 2004 Matthias Saou <http://freshrpms.net> 1.0-0.RC2.0
- Update to 1.0-RC2.
- Updated cdr patch, one fix made it upstream.

* Thu Jul 29 2004 Matthias Saou <http://freshrpms.net> 1.0-0.RC1.5
- Added Areski's cdr patch -2.
- Fix /var/run/asterisk -3.
- Change sample install to use the Makefile -4.
- Fix safe_asterisk -5.

* Mon Jul 26 2004 Matthias Saou <http://freshrpms.net> 1.0-0.RC1.1
- Update to 1.0-RC1.

* Thu Feb  5 2004 Matthias Saou <http://freshrpms.net> 0.7.2-1
- Update to 0.7.2.

* Tue Dec  2 2003 Matthias Saou <http://freshrpms.net>
- Updated to today's CVS code.
- Added asterisk-addons (cdr_addon_mysql).

* Tue Nov  4 2003 Matthias Saou <http://freshrpms.net>
- Added CVS release support.
- Changed ownership of the config directory to asterisk user.

* Fri Sep 19 2003 Matthias Saou <http://freshrpms.net>
- Initial RPM release.

