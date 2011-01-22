%define branch 0
%{?_branch: %{expand: %%global branch 1}}

%define epoch_arts 30000001

%if %branch
%define kde_snapshot git20101121
%endif

%define rel 1

Name: phonon
Summary: KDE4 Multimedia Framework 
Version: 4.4.4
%if %branch
Release: %mkrel -c %kde_snapshot %rel
%else
Release: %mkrel %rel
%endif
Epoch: 2
Url: http://phonon.kde.org/
License: LGPLv2+
Group: Graphical desktop/KDE
BuildRoot: %{_tmppath}/%{name}-%{version}-build
# We're using git: http://gitorious.org/phonon
%if %branch
Source0: phonon-%{version}-%{kde_snapshot}.tar.xz
%else
Source0: ftp://ftp.kde.org/pub/kde/stable/phonon/%version/%name-%version.tar.bz2
%endif
Patch1:  phonon-4.3.50-phonon-allow-stop-empty-source.patch
# (cg) NB This version hack is only needed for 2010.0... added here too for ease of backporting
Patch4:  phonon-4.3.80-ignore-pulse-version.patch

# (cg) Phonon 4.4.1 needs Qt 4.6+
BuildRequires:  qt4-devel >= 4:4.6
BuildRequires:  kde4-macros
BuildRequires:  automoc
BuildRequires:	glib2-devel
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

#--------------------------------------------------------------------

%package   devel
Group:     Development/KDE and Qt
Summary:   Header files and documentation for compiling KDE applications
Requires:  %libphononexperimental = %epoch:%version
Requires:  %libphonon = %epoch:%version
Conflicts: kdelibs4-devel < 4.0.80-5
Obsoletes: phonon-common
%if %mdkversion >= 201000
Obsoletes: arts-devel < %epoch_arts:1.5.10-9
Obsoletes: arts3-devel < %epoch_arts:1.5.10-9
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
%{_kde_datadir}/phonon-buildsystem
%{_kde_datadir}/dbus-1/interfaces/org.kde.Phonon.AudioOutput.xml
%{qt4dir}/mkspecs/modules/qt_phonon.pri

#--------------------------------------------------------------------

%prep
%if %branch
%setup -q  -n %name
%else
%setup -q  -n %name-%version
%endif
%apply_patches

%build
%cmake_kde4 \
	-DUSE_INSTALL_PLUGIN=TRUE

%make

%install
rm -fr %buildroot
%makeinstall_std -C build

%clean
rm -rf "%{buildroot}"

