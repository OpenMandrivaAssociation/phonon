Name:           phonon
Summary:        KDE4 Multimedia Framework 
Version:        4.2.0
Release:        %mkrel 7
Url:            http://phonon.kde.org/
License:        LGPLv2+
Group:          Graphical desktop/KDE
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source0: ftp://ftp.kde.org/pub/kde/stable/%name/%version/%name-%version.tar.bz2
Patch0: phonon-4.2.0-branch-diff-855994.patch
BuildRequires:  qt4-devel
BuildRequires:  kde4-macros
BuildRequires:  automoc
BuildRequires:  glib2-devel
BuildRequires:  libxml2-devel

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
Provides: phonon-backend = %version

%description -n phonon-gstreamer
GStreamer backend to Phonon.

%files -n phonon-gstreamer
%defattr(-,root,root)
%_kde_libdir/kde4/plugins/phonon_backend/*
%_kde_datadir/kde4/services/phononbackends/gstreamer.desktop
%attr(0755,root,root) %_sysconfdir/profile.d/55phonon-gstreamer.*

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

%build
%cmake_kde4
%make

%install
rm -fr %buildroot
%makeinstall_std -C build

# Profiles for gstreamer auto
mkdir -p %buildroot%_sysconfdir/profile.d
cat > %buildroot%_sysconfdir/profile.d/55phonon-gstreamer.sh << EOF
#!/bin/bash

if [ -z \${PHONON_GST_AUDIOSINK} ]; then
    PHONON_GST_AUDIOSINK=autoaudiosink
    export PHONON_GST_AUDIOSINK
fi
EOF

cat > %buildroot%_sysconfdir/profile.d/55phonon-gstreamer.csh << EOF
if ! ( \$?PHONON_GST_AUDIOSINK ) then
    setenv PHONON_GST_AUDIOSINK autoaudiosink
endif
EOF

%clean
rm -rf "%{buildroot}"
