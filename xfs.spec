Name: xfs
Version: 1.0.5
Release: %mkrel 1
Summary: Font server for X11
Group: System/Servers
Source0: http://xorg.freedesktop.org/releases/individual/app/%{name}-%{version}.tar.bz2
Source1: xfs.init
Source2: xfs.sysconfig
Source3: xfs.config
Patch0: xfs-1.0.4-fontpath_d.patch
Patch1: xfs-fix-handling-of-invalid-non-path-FPE.patch
License: MIT

BuildRequires: libfs-devel >= 1.0.0
BuildRequires: libxfont-devel >= 1.2.8-2mdv
BuildRequires: x11-util-macros >= 1.0.1
BuildRequires: x11-xtrans-devel >= 1.0.0

Requires(pre): rpm-helper 
Requires(post): rpm-helper 
Requires: fslsfonts
Requires: fstobdf
Requires: showfont

# because of X11R6 directory handling on x11-server-common
Requires(pre): x11-server-common >= 1.3.0.0-8mdv

# because of fontpath.d support
Requires: libxfont >= 1.2.8-2mdv

%description
This is a font server for X11.  You can serve fonts to other X servers
remotely with this package, and the remote system will be able to use all
fonts installed on the font server, even if they are not installed on the
remote computer.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .fontpath-symlinks
%patch1 -p1 -b .fix-non-path-fontpath-fatal-error

%build
autoreconf -i
%configure

%make configdir=%{_sysconfdir}/X11/fs

%install
rm -rf %{buildroot}
%makeinstall_std configdir=%{_sysconfdir}/X11/fs

# initscript
mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d/
install -m 0755 %{SOURCE1} %{buildroot}%{_sysconfdir}/rc.d/init.d/xfs
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig/
install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/xfs

# config
# remove the default
rm -f %{buildroot}%{_sysconfdir}/X11/fs/config
#install ours
install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/X11/fs/config

# add backward compatibility link for /usr/lib/X11/fs (#23423)
install -d -m 755 %{buildroot}%{_libdir}/X11/
ln -s ../../../%{_sysconfdir}/X11/fs %{buildroot}%{_libdir}/X11/fs

%pre
%_pre_useradd xfs /etc/X11/fs /bin/false

# for msec high security levels
%_pre_groupadd xgrp xfs


%post
%_post_service xfs

# handle init sequence change
if [ -f /etc/rc5.d/S90xfs ] && grep -q 'chkconfig: 2345 20 10' /etc/init.d/xfs; then
	/sbin/chkconfig --add xfs
fi

%preun
%_preun_service xfs

%postun
%_postun_userdel xfs

%triggerpostun -- XFree86-xfs
%_post_service xfs
if [ ! -f /var/lock/subsys/xfs ]
then
  /sbin/service xfs start
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(-,xfs,xfs) %dir %{_sysconfdir}/X11/fs
%{_libdir}/X11/fs
%{_bindir}/xfs
%{_mandir}/man1/xfs.*
%attr(-,xfs,xfs) %config(noreplace) %{_sysconfdir}/X11/fs/config
%dir %{_sysconfdir}/X11/fontpath.d
%{_sysconfdir}/rc.d/init.d/xfs
%{_sysconfdir}/sysconfig/xfs

