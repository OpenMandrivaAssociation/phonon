%define major 4

Name:		phonon
Summary:	KDE4 Multimedia Framework 
Group:		Graphical desktop/KDE
Version:	4.6.0
Release:	8
Epoch:		2
URL:		http://phonon.kde.org/
License:	LGPLv2+
Source0:	ftp://ftp.kde.org/pub/kde/stable/phonon/%{version}/%{name}-%{version}.tar.xz
Patch1:		phonon-4.6.50-phonon-allow-stop-empty-source.patch
Patch2:		phonon-4.6.0-qmake-syntax.patch
# (cg) NB This version hack is only needed for 2010.0... added here too for ease of backporting
Source4:	phonon-4.3.80-ignore-pulse-version.patch
# (cg) Phonon 4.4.1 needs Qt 4.6+
BuildRequires:	cmake
BuildRequires:	imagemagick
BuildRequires:	automoc4
BuildRequires:	qt4-devel >= 4:4.6
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(libpulse)

%description
Phonon is the KDE4 Multimedia Framework

#--------------------------------------------------------------------
%define libphononexperimental %mklibname phononexperimental %{major}

%package -n %{libphononexperimental}
Summary:	Phonon Library
Group:		System/Libraries

%description -n %{libphononexperimental}
Library for Phonon.

%files -n %{libphononexperimental}
%{_libdir}/libphononexperimental.so.%{major}*

#--------------------------------------------------------------------
%define libphonon %mklibname phonon %{major}

%package -n %{libphonon}
Summary:	Phonon Library
Group:		System/Libraries

%description -n %{libphonon}
Library for Phonon.

%files -n %{libphonon}
%{_libdir}/libphonon.so.%{major}*

#--------------------------------------------------------------------
%package designer-plugin
Summary:	Phonon Designer Plugin
Group:		System/Libraries
Conflicts:	qt4-designer-plugin-phonon <= 5:4.7.4

%description designer-plugin
Designer plugin for phonon.

%files designer-plugin
%{_qt_plugindir}/designer/libphononwidgets.so

#--------------------------------------------------------------------
%package devel
Group:		Development/KDE and Qt
Summary:	Phonon Development Files
Requires:	%{libphononexperimental} = %{EVRD}
Requires:	%{libphonon} = %{EVRD}
Requires:	phonon-designer-plugin = %{EVRD}

%description devel
Header files needed to compile applications for KDE.

%files devel
%{_qt_datadir}/mkspecs/modules/qt_phonon.pri
%{_datadir}/dbus-1/interfaces/org.kde.Phonon.AudioOutput.xml
%{_datadir}/phonon/buildsystem/
%{_includedir}/phonon/
%{_includedir}/KDE/
%{_libdir}/libphonon.so
%{_libdir}/libphononexperimental.so
%{_libdir}/pkgconfig/phonon.pc
%{_libdir}/cmake/phonon/Phonon*.cmake

#--------------------------------------------------------------------
%prep
%setup -q
%apply_patches

%build
%cmake \
    -DPHONON_INSTALL_QT_EXTENSIONS_INTO_SYSTEM_QT=ON
%make

%install
%makeinstall_std -C build



%changelog
* Wed May 23 2012 Andrey Bondrov <abondrov@mandriva.org> 2:4.6.0-2
+ Revision: 800225
- Add patch 2 to fix incorrect qmake syntax in qt_phonon.pri (KDE bug 295037)

* Thu Dec 22 2011 Zé <ze@mandriva.org> 2:4.6.0-1
+ Revision: 744298
- needs cmake
- use cmake macro to build
- fix summaries and descriptions
- 4.6.0
- phonon doesnt need to use kde4 macros,theres no need to change instalation path since only appeared in kde 4 and is compatible also with kde 5, it will never be needed to move phonon localtion
- allow user to install or not phonon plugin (independently of isntall devel package
- updae patch1
- patch4 isnt needed anymore bu still is kept as a source

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - drop deprecated scriptlets

* Thu May 12 2011 Funda Wang <fwang@mandriva.org> 2:4.5.0-4
+ Revision: 673883
- really obsoletes

* Thu May 12 2011 Funda Wang <fwang@mandriva.org> 2:4.5.0-3
+ Revision: 673724
- rename old name

* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 2:4.5.0-2
+ Revision: 667474
- mass rebuild

  + Nicolas Lécureuil <nlecureuil@mandriva.com>
    - Update to version 4.5.0

* Sat Jan 22 2011 Funda Wang <fwang@mandriva.org> 2:4.4.4-1
+ Revision: 632260
- New version 4.4.4

  + John Balcaen <mikala@mandriva.org>
    - imported package phonon

* Sun Nov 28 2010 Funda Wang <fwang@mandriva.org> 2:4.4.3-1mdv2011.0
+ Revision: 602172
- 4.4.3 final

* Wed Nov 24 2010 Funda Wang <fwang@mandriva.org> 2:4.4.3-0.git20101121.1mdv2011.0
+ Revision: 600373
- new snapshot

* Tue Sep 14 2010 Funda Wang <fwang@mandriva.org> 2:4.4.3-0.git20100914.1mdv2011.0
+ Revision: 578245
- New snapshot needed by kdebase4-runtime

* Tue Aug 17 2010 Colin Guthrie <cguthrie@mandriva.org> 2:4.4.2-2mdv2011.0
+ Revision: 571007
- Protect pulseaudio detection probe from multi-thread startup (maybe helps bko#232068

  + Stéphane Laurière <slauriere@mandriva.com>
    - Added missing spaces to the declaration of the devel package's obsoletes (#60148)

* Tue Jul 13 2010 Colin Guthrie <cguthrie@mandriva.org> 2:4.4.2-1mdv2011.0
+ Revision: 552936
- New version: 4.4.2

* Wed May 12 2010 Colin Guthrie <cguthrie@mandriva.org> 2:4.4.1-6mdv2010.1
+ Revision: 544572
- Add some fixes related to mdv #59052

* Mon May 10 2010 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.4.1-5mdv2010.1
+ Revision: 544364
- Use decodebin instead of decodebin2

* Fri May 07 2010 Colin Guthrie <cguthrie@mandriva.org> 2:4.4.1-4mdv2010.1
+ Revision: 543266
- Maybe fix a problem with incorrect error notification on startup with PA

* Tue Apr 27 2010 Christophe Fergeau <cfergeau@mandriva.com> 2:4.4.1-3mdv2010.1
+ Revision: 539591
- rebuild so that shared libraries are properly stripped again

* Sat Apr 24 2010 Colin Guthrie <cguthrie@mandriva.org> 2:4.4.1-2mdv2010.1
+ Revision: 538491
- Fix a couple problems with PA integration (bko#235193)

* Thu Apr 22 2010 Colin Guthrie <cguthrie@mandriva.org> 2:4.4.1-1mdv2010.1
+ Revision: 537855
- New version: 4.4.1

* Mon Apr 05 2010 Colin Guthrie <cguthrie@mandriva.org> 2:4.3.80-10.20100330.2mdv2010.1
+ Revision: 531604
- Fix UTF8 encoding in PA support. Mdv#57159

* Wed Mar 31 2010 Colin Guthrie <cguthrie@mandriva.org> 2:4.3.80-10.20100330.1mdv2010.1
+ Revision: 530081
- Update to latest git with PulseAudio per-application volume support.
- Drop upstream applied patch

* Wed Mar 17 2010 Colin Guthrie <cguthrie@mandriva.org> 2:4.3.80-10.20100317.1mdv2010.1
+ Revision: 524723
- Update to phonon git master.
- Drop merged patches
- Add PA connection rework (bko#228324)

* Thu Mar 11 2010 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.3.80-7mdv2010.1
+ Revision: 518012
- Remove requires in gstreamer0.10-plugins-ugly
- Add comment about patch2 merged upstream
- add infos for next update

* Wed Feb 03 2010 Colin Guthrie <cguthrie@mandriva.org> 2:4.3.80-6mdv2010.1
+ Revision: 499849
- Rework device moving on a system with PA underneath
- Remove version from the phonon-backend provide as it's not of any practical value

* Sun Jan 24 2010 Colin Guthrie <cguthrie@mandriva.org> 2:4.3.80-5mdv2010.1
+ Revision: 495602
- Fix an issue with pulsecleanup patch relating to startup configuration

* Sat Jan 23 2010 Colin Guthrie <cguthrie@mandriva.org> 2:4.3.80-4mdv2010.1
+ Revision: 495317
- Add a PA cleanup patch for wider debugging
- Use %%apply_patches macro (easier to manage)
- Update tarball to svn trunk
- Drop merged patches
- Fix xine output with PA under some error conditions

* Thu Jan 21 2010 Colin Guthrie <cguthrie@mandriva.org> 2:4.3.80-3mdv2010.1
+ Revision: 494635
- Fix another problem with gst backend relating to play->stop->play on a media object with PulseAudio (possibly alsa too)

* Thu Jan 14 2010 Colin Guthrie <cguthrie@mandriva.org> 2:4.3.80-2mdv2010.1
+ Revision: 491078
- Remove unsed (and already applied upstream) patch
- Hopefully fix mdv#56807 (randomly disappearing sound under KDE+PA)

* Sun Dec 27 2009 Funda Wang <fwang@mandriva.org> 2:4.3.80-1mdv2010.1
+ Revision: 482675
- New version 4.3.80

* Mon Nov 23 2009 Colin Guthrie <cguthrie@mandriva.org> 2:4.3.50-21mdv2010.1
+ Revision: 469160
- Make sure pulseaudio stream moves are processed on reused streams.
- Remove old pulseaudio patch

* Sun Nov 22 2009 Colin Guthrie <cguthrie@mandriva.org> 2:4.3.50-20mdv2010.1
+ Revision: 469037
- Update to phonon trunk
- Remove four upstream-applied patches
- Remove version check on PulseAudio version (we know ours is OK)
- Renumber patches

* Sun Nov 15 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.3.50-19mdv2010.1
+ Revision: 466199
- Add requires on gstreamer-ugly, that fix the time bar in amarok

* Tue Oct 27 2009 Colin Guthrie <cguthrie@mandriva.org> 2:4.3.50-18mdv2010.0
+ Revision: 459458
- Some updates/fixes relating to pulseaudio support
-  Ensure the stream is moved when the device priorities change
-  Ensure the UI parts are correctly called to inform the user of whats happened when the device changes.
-  Add some extra debug

  + Nicolas Lécureuil <nlecureuil@mandriva.com>
    - Use decodebin2 instead of decodebin
      Use playbin2 instead of playbin
      BUG:51955

* Sat Oct 24 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.3.50-16mdv2010.0
+ Revision: 459181
- Add DVD support in the Gstreamer engine

* Sun Oct 18 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.3.50-15mdv2010.0
+ Revision: 458069
- Add xine-pulse as Suggests in phonon-xine

* Fri Oct 16 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.3.50-14mdv2010.0
+ Revision: 457859
- Add gstreamer0.10-pulse as suggests

* Thu Oct 15 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.3.50-13mdv2010.0
+ Revision: 457487
- Fix seekable streams

* Thu Oct 15 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.3.50-12mdv2010.0
+ Revision: 457485
- Add patches fixing the gstreamer engine

* Sun Oct 11 2009 Colin Guthrie <cguthrie@mandriva.org> 2:4.3.50-11mdv2010.0
+ Revision: 456615
- Fix xine output after latest changes.

* Sat Oct 10 2009 Colin Guthrie <cguthrie@mandriva.org> 2:4.3.50-10mdv2010.0
+ Revision: 456561
- Update PulseAudio support

* Sat Oct 03 2009 Colin Guthrie <cguthrie@mandriva.org> 2:4.3.50-9mdv2010.0
+ Revision: 453182
- Latest version of pulseaudio support
-  o Category priority lists now work.
-  o Notifications are sent when devices are added/removed.
- Drop upstream applied patches
- Update to trunk r1030942

* Fri Oct 02 2009 Colin Guthrie <cguthrie@mandriva.org> 2:4.3.50-8mdv2010.0
+ Revision: 452493
- Latest version of PulseAudio support patch (routing and priority now working for the 'No Category' case)

  + Nicolas Lécureuil <nlecureuil@mandriva.com>
    - Fix requires for phonon-gstreamer

  + Helio Chissini de Castro <helio@mandriva.com>
    - Update to phonon trunk latest source.
    - Remove current gst patch, as already included upstream by Colin

* Thu Sep 24 2009 Colin Guthrie <cguthrie@mandriva.org> 2:4.3.50-6mdv2010.0
+ Revision: 448193
- Add some fixes I pushed upstream for gstreamer device enumeration and backend reloading

* Wed Sep 23 2009 Colin Guthrie <cguthrie@mandriva.org> 2:4.3.50-5mdv2010.0
+ Revision: 447872
- Package eating monster munched -devel on i586... rebuild

* Wed Sep 23 2009 Colin Guthrie <cguthrie@mandriva.org> 2:4.3.50-4mdv2010.0
+ Revision: 447819
- Update pulseaudio patch slightly due to a copy paste error
- Revised pulseaudio detection patch that does not rely on Mandriva specific configs (that have been deprecated anyway)

* Mon Sep 21 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.3.50-3mdv2010.0
+ Revision: 446954
- Add patch from lmenut to support more that one CD/DVD driver

* Mon Sep 14 2009 Helio Chissini de Castro <helio@mandriva.com> 2:4.3.50-2mdv2010.0
+ Revision: 440619
- Byte your own tongue.. Add api support in trunk and forget to enable it in your own distro :-P

* Mon Sep 14 2009 Helio Chissini de Castro <helio@mandriva.com> 2:4.3.50-1mdv2010.0
+ Revision: 440615
- Use phonon trunk
- Removed backported trunk patches
- Added api and stream extract data patches in trunk

* Thu Sep 03 2009 Helio Chissini de Castro <helio@mandriva.com> 2:4.3.1-15mdv2010.0
+ Revision: 428957
- Removed implicit requires to pulse modules.

* Sat Aug 15 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.3.1-14mdv2010.0
+ Revision: 416458
- Fix typo
- Obsolete kde3 arts

* Thu Jun 04 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 2:4.3.1-13mdv2010.0
+ Revision: 382891
- Revert to phonon 4.3.1

* Sat May 30 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 1:4.3.50-0.975368.1mdv2010.0
+ Revision: 381233
- New snapshot
  Remove merged patches
  Rediff patches

* Thu May 28 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 1:4.3.1-12mdv2010.0
+ Revision: 380599
- Add patch from trunk to add equalizer effect in the xine engine

* Mon Apr 06 2009 Helio Chissini de Castro <helio@mandriva.com> 1:4.3.1-11mdv2009.1
+ Revision: 364421
- Remove extra suggests

* Fri Apr 03 2009 Helio Chissini de Castro <helio@mandriva.com> 1:4.3.1-10mdv2009.1
+ Revision: 363821
- phonon is not the place to obsolete arts

* Fri Mar 20 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 1:4.3.1-9mdv2009.1
+ Revision: 358263
- [Trunk] Add features in gstreamer engine
- Fix versionnate

* Wed Mar 18 2009 Helio Chissini de Castro <helio@mandriva.com> 1:4.3.1-7mdv2009.1
+ Revision: 357377
- Add initial support for gstreamer install plugins codec api, in a generic mode.
  This will allow default usage of Codeina or any helper script app as defined in the gstreamer compilation
- Removed old invalid patch

* Wed Mar 18 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 1:4.3.1-6mdv2009.1
+ Revision: 357305
- Fix obsoletes

* Tue Mar 17 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 1:4.3.1-5mdv2009.1
+ Revision: 356960
- Obsolete old arts

* Mon Mar 16 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 1:4.3.1-4mdv2009.1
+ Revision: 356217
- Remove subrel
  Bump release
- Add missing patch
- Add one revision per patch
- fix typo

* Fri Mar 06 2009 Colin Guthrie <cguthrie@mandriva.org> 1:4.3.1-3mdv2009.1
+ Revision: 349544
- Make strings translatable

* Sat Feb 28 2009 Helio Chissini de Castro <helio@mandriva.com> 1:4.3.1-2mdv2009.1
+ Revision: 346054
- Added backports patc for enconding fix.
- Added backport patch to stop/pause issue long seen in Amarok

* Fri Feb 27 2009 Helio Chissini de Castro <helio@mandriva.com> 1:4.3.1-1mdv2009.1
+ Revision: 345512
- Phonon 4.3.1 try#1 upstream release

* Mon Feb 23 2009 Colin Guthrie <cguthrie@mandriva.org> 1:4.3.0-2mdv2009.1
+ Revision: 344017
- Do not list any other devices when pulseaudio is enabled
- Pulseaudio is not an advanced output (patch seems to have been misconceived)

* Thu Jan 22 2009 Helio Chissini de Castro <helio@mandriva.com> 1:4.3.0-1mdv2009.1
+ Revision: 332566
- New upstream release tied to 4.2.0 upcoming release
- Fixed tarball from upstream

* Fri Jan 09 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 1:4.2.96-1mdv2009.1
+ Revision: 327543
- New version 4.2.96

* Thu Dec 18 2008 Colin Guthrie <cguthrie@mandriva.org> 1:4.2.80-1.895450.2mdv2009.1
+ Revision: 315395
- Fix URL parsing (e.g. when [ or ] in the name). Fixes mdv#45950

* Wed Dec 10 2008 Nicolas Lécureuil <nlecureuil@mandriva.com> 1:4.2.80-1.895450.1mdv2009.1
+ Revision: 312583
- Fix Release
- Update to new snapshot

* Mon Nov 24 2008 Helio Chissini de Castro <helio@mandriva.com> 1:4.2.80-1mdv2009.1
+ Revision: 306420
- Updated with fresh beta 1 official tarball

* Sun Oct 19 2008 Nicolas Lécureuil <nlecureuil@mandriva.com> 1:4.2.70-0.866326.2mdv2009.1
+ Revision: 295414
- Add epoch to ease upgrade
- New snapshot
- New snapshot

* Sun Oct 19 2008 Colin Guthrie <cguthrie@mandriva.org> 4.2.0-14mdv2009.1
+ Revision: 295176
- Slightly better patch that also handles .oga files
- Fix .ogg mime type handling

* Fri Oct 03 2008 Helio Chissini de Castro <helio@mandriva.com> 4.2.0-13mdv2009.0
+ Revision: 291038
- added suggests for gstreamer plugins, allow uswers to have strea and mp3 as default

* Tue Sep 23 2008 Colin Guthrie <cguthrie@mandriva.org> 4.2.0-12mdv2009.0
+ Revision: 287159
- Fix broken path in my previous patch generation
- Revised patch for streaming data extraction.

* Sun Sep 21 2008 Colin Guthrie <cguthrie@mandriva.org> 4.2.0-11mdv2009.0
+ Revision: 286376
- Add a gstreamer icon
- Add a patch that requests metadata from streams via icydemux and
  fudge this info into ALBUM/ARTIST metadata.

* Sat Sep 20 2008 Colin Guthrie <cguthrie@mandriva.org> 4.2.0-10mdv2009.0
+ Revision: 286057
- Use the same icon as the xine icon for pulseaudio (yet to be supplied)
- Require gstreamer0.10-pulse in the gstreamer backend.

* Fri Sep 19 2008 Colin Guthrie <cguthrie@mandriva.org> 4.2.0-9mdv2009.0
+ Revision: 285790
- Update patch to use QSettings rather than KConfig (which was a silly idea in the first place)
- Add cosmetic patch for pulseaudio with gst backend (detect pulse via draksound settings)
- Remove profile.d env var setting scripts as this is now handled in pulseaudio patch

* Thu Sep 18 2008 Colin Guthrie <cguthrie@mandriva.org> 4.2.0-8mdv2009.0
+ Revision: 285742
- Set the glib application name for the benefit of gstreamer sink (app name is used by pulseaudio)

* Mon Sep 15 2008 Helio Chissini de Castro <helio@mandriva.com> 4.2.0-7mdv2009.0
+ Revision: 285032
- auto audio sink

* Sun Sep 14 2008 Helio Chissini de Castro <helio@mandriva.com> 4.2.0-6mdv2009.0
+ Revision: 284616
- Proper sink namex

* Sun Sep 14 2008 Helio Chissini de Castro <helio@mandriva.com> 4.2.0-5mdv2009.0
+ Revision: 284611
- Pulse as a default audiosink in gstreamer

* Tue Sep 02 2008 Helio Chissini de Castro <helio@mandriva.com> 4.2.0-4mdv2009.0
+ Revision: 279060
- update with latest branch with fixes

* Thu Aug 14 2008 Nicolas Lécureuil <nlecureuil@mandriva.com> 4.2.0-3mdv2009.0
+ Revision: 271687
- Add patch from trunk

* Wed Jul 30 2008 Helio Chissini de Castro <helio@mandriva.com> 4.2.0-2mdv2009.0
+ Revision: 255126
- Add version to phonon-backend provides, to avoid apps requires phonon < 4.2

* Thu Jul 24 2008 Funda Wang <fwang@mandriva.org> 4.2.0-1mdv2009.0
+ Revision: 246522
- 4.2.0 final

  + Helio Chissini de Castro <helio@mandriva.com>
    - Cleaning my mess

* Tue Jun 10 2008 Helio Chissini de Castro <helio@mandriva.com> 4.2-0.819157.1mdv2009.0
+ Revision: 217666
- Update phonon and fix devel install

* Tue Jun 03 2008 Helio Chissini de Castro <helio@mandriva.com> 4.2-0.815960.1mdv2009.0
+ Revision: 214437
- Enable gstreamer backend. Plugins now provides a virtual phonon-backend and main desktop will requires
  a phonon-backend instead of explicit one.
- Created phonon-common for dbus interfaces

* Thu May 29 2008 Nicolas Lécureuil <nlecureuil@mandriva.com> 4.2-0.814039.2mdv2009.0
+ Revision: 213136
- Comment a buildRequire
- Add BuildRequires
  Add TODO
- import phonon


