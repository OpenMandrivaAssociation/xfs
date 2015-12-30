%define _disable_rebuild_configure 1

Name:		xfs
Version:	1.1.4
Release:	3
Summary:	Font server for X11
Group:		System/Servers
Source0:	http://xorg.freedesktop.org/releases/individual/app/%{name}-%{version}.tar.bz2
Source1:	xfs.init
Source2:	xfs.sysconfig
Source3:	xfs.config
License:	MIT
Obsoletes:	xorg-x11-xfs

BuildRequires:	libfs-devel >= 1.0.0
BuildRequires:	libxfont-devel >= 1.2.8-2mdv
BuildRequires:	x11-util-macros >= 1.0.1
BuildRequires:	x11-xtrans-devel >= 1.0.0

Requires(pre):	rpm-helper 
Requires(post):	rpm-helper 
Requires:	fslsfonts
Requires:	fstobdf
Requires:	showfont

# because of X11R6 directory handling on x11-server-common
Requires(pre):	x11-server-common >= 1.4.0.90-13mdv

# because of fontpath.d support
Requires:	libxfont >= 1.2.8-2mdv

%define fontpath %{_sysconfdir}/X11/fontpath.d

%description
This is a font server for X11.  You can serve fonts to other X servers
remotely with this package, and the remote system will be able to use all
fonts installed on the font server, even if they are not installed on the
remote computer.

%prep
%setup -q -n %{name}-%{version}

%build
%configure2_5x	\
		--with-default-font-path=%{fontpath} \
		--disable-devel-docs

%make configdir=%{_sysconfdir}/X11/fs

%install
%makeinstall_std configdir=%{_sysconfdir}/X11/fs

install -d 755 %{buildroot}%{fontpath}

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

%files
%attr(-,xfs,xfs) %dir %{_sysconfdir}/X11/fs
%{_libdir}/X11/fs
%{_bindir}/xfs
%{_mandir}/man1/xfs.*
%attr(-,xfs,xfs) %config(noreplace) %{_sysconfdir}/X11/fs/config
%dir %{_sysconfdir}/X11/fontpath.d
%{_sysconfdir}/rc.d/init.d/xfs
%{_sysconfdir}/sysconfig/xfs



%changelog
* Sat May 07 2011 Oden Eriksson <oeriksson@mandriva.com> 1.1.1-2mdv2011.0
+ Revision: 671314
- mass rebuild

* Tue Nov 02 2010 Thierry Vignaud <tv@mandriva.org> 1.1.1-1mdv2011.0
+ Revision: 592587
- new release

* Fri Nov 13 2009 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 1.1.0-3mdv2010.1
+ Revision: 465885
+ rebuild (emptylog)

* Thu Jul 09 2009 Ander Conselvan de Oliveira <ander@mandriva.com> 1.1.0-2mdv2010.0
+ Revision: 393919
- xfs.init: fix restart option (mdv #51826)

* Fri Jun 19 2009 Ander Conselvan de Oliveira <ander@mandriva.com> 1.1.0-1mdv2010.0
+ Revision: 387400
- update to version 1.1.0

* Mon Jun 30 2008 Ander Conselvan de Oliveira <ander@mandriva.com> 1.0.8-2mdv2009.0
+ Revision: 230403
- Bump release number
- Revert commits 207239 and 201454. Move back configuration to %%{_sysconfdir}/X11

* Tue May 27 2008 Colin Guthrie <cguthrie@mandriva.org> 1.0.8-1mdv2009.0
+ Revision: 211786
- New version

* Tue May 27 2008 Colin Guthrie <cguthrie@mandriva.org> 1.0.7-1mdv2009.0
+ Revision: 211772
- New version

* Wed May 14 2008 Paulo Andrade <pcpa@mandriva.com.br> 1.0.6-3mdv2009.0
+ Revision: 207239
- Move configuration files from %%{_sysconfdir}/11 to %%{_datadir}/X11.

* Mon May 05 2008 Paulo Andrade <pcpa@mandriva.com.br> 1.0.6-2mdv2009.0
+ Revision: 201454
- Don't try to make a link from /usr/lib/X11 to /etc/X11, as now /usr/lib/X11
  itself is a link to /etc/X11.

* Mon Apr 14 2008 Thierry Vignaud <tv@mandriva.org> 1.0.6-1mdv2009.0
+ Revision: 192973
- new release

* Thu Feb 14 2008 Paulo Andrade <pcpa@mandriva.com.br> 1.0.5-3mdv2008.1
+ Revision: 168574
- Close #35651 (error while upgrading from 2006 to 2008.0)
- Revert to use upstream tarball, build requires and remove non mandatory local patches.

* Fri Jan 18 2008 Paulo Andrade <pcpa@mandriva.com.br> 1.0.5-2mdv2008.1
+ Revision: 154738
- Updated BuildRequires and resubmit package.

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Oct 03 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 1.0.5-1mdv2008.0
+ Revision: 94976
- new upstream version: 1.0.5 (security fixes only)
- remove part of the fontpath_d patch which is
  already upstream (documentation)
  Official announce:
  http://lists.freedesktop.org/archives/xorg-announce/2007-October/000415.html

* Fri Jul 06 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 1.0.4-13mdv2008.0
+ Revision: 49037
- remove from config file fontpaths which were already
  added to fontpath.d

* Thu Jul 05 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 1.0.4-12mdv2008.0
+ Revision: 48665
- xfs is not required by dm anymore, so we can remove the
  XXX workaround from %%preun

* Thu Jul 05 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 1.0.4-11mdv2008.0
+ Revision: 48659
- remove X11/fs symlink dir extra level (fix #31760)

* Thu Jul 05 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 1.0.4-10mdv2008.0
+ Revision: 48584
- bah, I need some oil on my rpm skills :-)
  (fix version on requirement for x11-server-common)

* Thu Jul 05 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 1.0.4-9mdv2008.0
+ Revision: 48564
- due to the /usr/X11R6/ directory handling, add Requires(pre)
  for x11-server-common, otherwise an upgrade from old distros
  won't be reliable (thanks Pixel).

* Mon Jul 02 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 1.0.4-8mdv2008.0
+ Revision: 47204
- remove %%post section that was dealing with X11R6 legacy directory.
  It's now properly handled by x11-server-common (hopefuly) :)

* Fri Jun 22 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 1.0.4-7mdv2008.0
+ Revision: 43218
- remove drakfont paths from xfs.config (drakconf calls chkfontpath when
  adding fonts, so this hardcoded value is unecessary);
- remove hardcoded otf/ and ttc/ font dirs, couldn't find where
  these came from, but the same rationale applies: packages should use
  chkfontpath when adding/removing font paths;
- minor spec cleanup: remove unecessary configure options.

* Thu Jun 21 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 1.0.4-6mdv2008.0
+ Revision: 42317
- add fix-handling-of-invalid-non-path-FPE.patch, so that the server won't
  exit if it finds a bogus fpe in the catalogue (it will just ignore the
  entry, as it was supposed to do).
- build-require new libxfont (the one with fontpath.d support)
- minor spec cleanup (configure macro, remove packager tag, etc)

* Wed Jun 20 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 1.0.4-5mdv2008.0
+ Revision: 41918
- duu, the previous release was innocuous, since the
  added patch (fontpath_d.patch) was not applied :/

* Wed Jun 20 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 1.0.4-4mdv2008.0
+ Revision: 41903
- add fontpath.d patch, now xfs supports catalogue:<dir>
  entries. See the updated manpage for details.

* Tue May 29 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 1.0.4-3mdv2008.0
+ Revision: 32683
- introduce /etc/sysconfig/xfs, allowing one to set the listen tcp
  port (bug #30584) and pass extra options for xfs.


* Wed Mar 07 2007 Gustavo Pichorim Boiko <boiko@mandriva.com> 1.0.4-2mdv2007.0
+ Revision: 134425
- Remove unused old drakfont paths (#22457)
- Remove old /usr/lib/X11/fonts paths
- Add some missing drakfont paths

* Thu Dec 14 2006 Thierry Vignaud <tvignaud@mandriva.com> 1.0.4-1mdv2007.1
+ Revision: 97064
- new release

  + Pixel <pixel@mandriva.com>
    - fix compatibility symlink on x86_64

* Tue Sep 19 2006 Pixel <pixel@mandriva.com> 1.0.2-12mdv2007.0
+ Revision: 61939
- do not provide nor obsolete xorg-x11-xfs which is still a package in 2007.0
- do not provide nor obsolete xorg-x11-xfs which is still a package in 2007.0
- before creating symlink ../../lib/X11 -> /usr/X11R6/lib/X11, ensure directory /usr/X11R6/lib exists

* Fri Sep 15 2006 Pixel <pixel@mandriva.com> 1.0.2-11mdv2007.0
+ Revision: 61465
- in some cases we can not symlink /usr/X11R6/lib/X11 to /usr/lib/X11 since pkg like multiarch-utils vivify it. in that case, creating symlink /usr/X11R6/lib/X11/fs to /usr/lib/X11/fs (and so /etc/X11/fs)
- creating /usr/X11R6/lib/X11 linked to /usr/lib/X11 for commercial applications (#23423)

* Thu Aug 24 2006 Antonio Hobmeir Neto <neto@mandriva.com> 1.0.2-9mdv2007.0
+ Revision: 57757
- Changed the word "Mandrake" per "Mandriva" in xfs.config (#21025)

* Tue Aug 22 2006 Pixel <pixel@mandriva.com> 1.0.2-8mdv2007.0
+ Revision: 56957
- better handle fs/config migration to /usr/share/fonts in a trigger in xorg-x11-xfs

* Fri Aug 18 2006 Pixel <pixel@mandriva.com> 1.0.2-7mdv2007.0
+ Revision: 56569
- (minor) increase release number
- fix migrating /etc/X11/fs/config directories to /usr/share/fonts

* Fri Aug 04 2006 Helio Chissini de Castro <helio@mandriva.com> 1.0.2-6mdv2007.0
+ Revision: 51500
- Added new place /usr/share/fonts. Approved by Boiko

  + Gustavo Pichorim Boiko <boiko@mandriva.com>
    - when restarting xfs be sure it starts as daemon (#23240)
    - handle the restart case when there is the /var/lock/subsys/xfs file but no
      xfs running (#11717)

* Tue Jul 04 2006 Gustavo Pichorim Boiko <boiko@mandriva.com> 1.0.2-4mdv2007.0
+ Revision: 38331
- Upload blino's fix for #23423
- rebuild to fix cooker uploading
- X11R7.1
- Add packager tag
- Remove the X11R6 from the font paths in /etc/X11/fs/config
- fixed xfs.config file to search for fonts in the new prefix
- removed the dependency on chkfontpath as it was causing a circular dependency
  involving pre-reqs
- the preun script doesn't work if the dm service is present, just returning
  true for now
- increment release
- fixed more dependencies
- Adding X.org 7.0 to the repository

  + Olivier Blin <oblin@mandriva.com>
    - add backward compatibility link for /usr/X11R6/lib/X11/fs (#23423)

  + Pascal Terjan <pterjan@mandriva.org>
    - return exit code for status in the initscript

  + Pixel <pixel@mandriva.com>
    - /etc/init.d/xfs is not a conf file
    - don't use PreReq
    - don't use _sourcedir
    - restart xfs *after* removing X11R6/ from the config file

  + Andreas Hasenack <andreas@mandriva.com>
    - renamed mdv to packages because mdv is too generic and it's hosting only packages anyway

