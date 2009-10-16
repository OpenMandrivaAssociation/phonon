%define epoch_arts 30000001
%define rev 1030942

Name: phonon
Summary: KDE4 Multimedia Framework 
Version: 4.3.50
Release: %mkrel 14
Epoch: 2
Url: http://phonon.kde.org/
License: LGPLv2+
Group: Graphical desktop/KDE
BuildRoot: %{_tmppath}/%{name}-%{version}-build
# We're using trunk http://svn.kde.org/home/kde/trunk/kdesupport/phonon
Source0: %name-%version.%{rev}.tar.bz2
Source1: %{name}-gstreamer.svg
Patch0:  phonon-4.2.0-ogg-mime-type.patch
# (cg) For the latest version of the below patch see: http://colin.guthr.ie/git/phonon/log/?h=pulse
Patch2:  phonon-4.3-pulseaudio.patch
Patch3:  phonon-4.3.50-phonon-allow-stop-empty-source.patch
Patch4:  phonon-4.3.50-gstreamer-fix-changing-CD-audio-track2.patch
Patch5:  phonon-4.3.50-gstreamer-fix-titles2.patch
Patch6:  phonon-4.3.50-gstreamer-fix-seekable-query-failed.patch
BuildRequires:  qt4-devel
BuildRequires:  kde4-macros
BuildRequires:  automoc
BuildRequires:  glib2-devel
BuildRequires:  libxml2-devel
BuildRequires:  imagemagick
BuildRequires:  pulseaudio-devel

%description
Phonon is the KDE4 Multimedia Framework

#--------------------------------------------------------------------

%define phononexperimental_major 4
%define libphononexperimental %mklibname phononexperimental %phononexperimental_major

%package -n %libphononexperimental
Summary: Phonon library
Group: System/Libraries
Conflicts: %{_lib}kdecore5 >= 30000000:3.80.3
Obsoletes: %{_lib}phononexperimental5 < 3.93.0-0.714006.1


%description -n %libphononexperimental
Phonon library.

%post -n %libphononexperimental -p /sbin/ldconfig
%postun -n %libphononexperimental -p /sbin/ldconfig

%files -n %libphononexperimental
%defattr(-,root,root)
%_kde_libdir/libphononexperimental.so.%{phononexperimental_major}*

#--------------------------------------------------------------------

%define phonon_major 4
%define libphonon %mklibname phonon %phonon_major

%package -n %libphonon
Summary: Phonon library
Group: System/Libraries
Conflicts: %{_lib}kdecore5 >= 30000000:3.80.3
Obsoletes: %{_lib}phonon5 < 3.93.0-0.714006.1

%description -n %libphonon
Phonon library.

%post -n %libphonon -p /sbin/ldconfig
%postun -n %libphonon -p /sbin/ldconfig

%files -n %libphonon
%defattr(-,root,root)
%_kde_libdir/libphonon.so.%{phonon_major}*

#-----------------------------------------------------------------------------

%package -n phonon-gstreamer
Summary: GStreamer backend to Phonon
Group: Sound
BuildRequires: libgstreamer-devel
BuildRequires: libgstreamer-plugins-base-devel
Requires: gstreamer0.10-plugins-good
Requires: gstreamer0.10-plugins-base
Suggests: gstreamer0.10-ffmpeg
Suggests: gstreamer0.10-soup
Suggests: gstreamer0.10-pulse
%if %mdkversion >= 201000
Obsoletes:      arts < %epoch_arts:1.5.10-9
Obsoletes:      arts3 < %epoch_arts:1.5.10-9
%endif

Provides: phonon-backend = %epoch:%version

%description -n phonon-gstreamer
GStreamer backend to Phonon.

%files -n phonon-gstreamer
%defattr(-,root,root)
%dir %_kde_libdir/kde4/plugins/phonon_backend
%_kde_libdir/kde4/plugins/phonon_backend/phonon_gstreamer.so
%_kde_datadir/kde4/services/phononbackends/gstreamer.desktop
%_datadir/icons/hicolor/*

#-----------------------------------------------------------------------------

%package -n phonon-xine
Summary: Xine backend to Phonon
Group: Sound
BuildRequires: libxine-devel
Obsoletes: kde4-phonon-xine < 1:3.93.0-0.714129.2
Requires: xine-plugins
Provides: phonon-backend = %epoch:%version

%description -n phonon-xine
Xine backend to Phonon.

%files -n phonon-xine
%defattr(-,root,root)
%dir %_kde_libdir/kde4/plugins/phonon_backend
%_kde_libdir/kde4/plugins/phonon_backend/phonon_xine.so
%_kde_datadir/kde4/services/phononbackends/xine.desktop
%_kde_iconsdir/*/*/*/phonon-xine.*

#--------------------------------------------------------------------

%package   devel
Group:     Development/KDE and Qt
Summary:   Header files and documentation for compiling KDE applications
Requires:  %libphononexperimental = %epoch:%version
Requires:  %libphonon = %epoch:%version
Conflicts: kdelibs4-devel < 4.0.80-5
Obsoletes: phonon-common
%if %mdkversion >= 201000
Obsoletes: arts-devel< %epoch_arts:1.5.10-9
Obsoletes: arts3-devel< %epoch_arts:1.5.10-9
%endif

%description devel
This package includes the header files you will need to compile applications
for KDE. Also included is the KDE API documentation in HTML format for easy
browsing.

%files devel
%defattr(-,root,root,-)
%{_kde_includedir}/phonon
%{_kde_includedir}/KDE
%{_kde_libdir}/libphonon.so
%{_kde_libdir}/libphononexperimental.so
%{_kde_libdir}/pkgconfig/phonon.pc
%{_kde_datadir}/dbus-1/interfaces/org.kde.Phonon.AudioOutput.xml

#--------------------------------------------------------------------

%prep
%setup -q  -n %name-%version
%patch0 -p0
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
%cmake_kde4 \
	-DUSE_INSTALL_PLUGIN=TRUE

%make

%install
rm -fr %buildroot
%makeinstall_std -C build

# Make a nice icon
install -D -m 0644 %{_sourcedir}/%{name}-gstreamer.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}-gstreamer.svg
for size in 16 22 32 48 64 128; do
  mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps
  convert -geometry ${size}x${size} %{_sourcedir}/%{name}-gstreamer.svg %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/%{name}-gstreamer.png
done

%clean
rm -rf "%{buildroot}"

