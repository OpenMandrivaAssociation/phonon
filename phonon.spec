Name:           phonon
Summary:        KDE4 Multimedia Framework 
Version:        4.2.0
Release:        %mkrel 13
Url:            http://phonon.kde.org/
License:        LGPLv2+
Group:          Graphical desktop/KDE
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source0: ftp://ftp.kde.org/pub/kde/stable/%name/%version/%name-%version.tar.bz2
Source1: %{name}-gstreamer.svg
Patch0: phonon-4.2.0-branch-diff-855994.patch
Patch1: phonon-4.2.0-set-glib-application-name.patch
Patch2: phonon-4.2.0-pulseaudio-detect-and-cosmetics.patch
Patch3: phonon-4.2.0-stream-extract-metadata.patch
BuildRequires:  qt4-devel
BuildRequires:  kde4-macros
BuildRequires:  automoc
BuildRequires:  glib2-devel
BuildRequires:  libxml2-devel
BuildRequires:  imagemagick

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
Requires: gstreamer0.10-pulse
Suggests: gstreamer0.10-plugins-ugly
Suggests: gstreamer0.10-ffmpeg
Suggests: gstreamer0.10-soup

Provides: phonon-backend = %version

%description -n phonon-gstreamer
GStreamer backend to Phonon.

%files -n phonon-gstreamer
%defattr(-,root,root)
%_kde_libdir/kde4/plugins/phonon_backend/*
%_kde_datadir/kde4/services/phononbackends/gstreamer.desktop
%_datadir/icons/hicolor/*

#--------------------------------------------------------------------

%package devel
Group: Development/KDE and Qt
Summary: Header files and documentation for compiling KDE applications
Requires: %libphononexperimental = %version
Requires: %libphonon = %version
Conflicts: kdelibs4-devel < 4.0.80-5
Obsoletes: phonon-common

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
%setup -q 
%patch0 -p1
%patch1 -p0
%patch2 -p0
%patch3 -p0

%build
%cmake_kde4
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
