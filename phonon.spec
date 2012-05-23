%define major 4
%define epoch_arts 30000001

Name:		phonon
Summary:	KDE4 Multimedia Framework 
Group:		Graphical desktop/KDE
Version:	4.6.0
Release:	2
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
BuildRequires:	qt4-devel >= 4:4.6
BuildRequires:	automoc4
BuildRequires:	glib2-devel
BuildRequires:	imagemagick
BuildRequires:	pulseaudio-devel

%description
Phonon is the KDE4 Multimedia Framework

#--------------------------------------------------------------------
%define libphononexperimental %mklibname phononexperimental %{major}

%package -n %{libphononexperimental}
Summary:	Phonon Library
Group:		System/Libraries
Conflicts:	%{_lib}kdecore5 >= 30000000:3.80.3
Obsoletes:	%{_lib}phononexperimental5 < 3.93.0-0.714006.1

%description -n %{libphononexperimental}
Library for Phonon.

%files -n %{libphononexperimental}
%{_libdir}/libphononexperimental.so.%{major}*

#--------------------------------------------------------------------
%define libphonon %mklibname phonon %{major}

%package -n %{libphonon}
Summary:	Phonon Library
Group:		System/Libraries
Conflicts:	%{_lib}kdecore5 >= 30000000:3.80.3
Obsoletes:	%{_lib}phonon5 < 3.93.0-0.714006.1

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
Conflicts:	kdelibs4-devel < 4.0.80-5
Obsoletes:	qt4-designer-plugin-phonon
Obsoletes:	phonon-common
%if %{mdkversion} >= 201000
Obsoletes:	arts-devel < %{epoch_arts}:1.5.10-9
Obsoletes:	arts3-devel < %{epoch_arts}:1.5.10-9
%endif

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
%__rm -fr %{buildroot}
%makeinstall_std -C build

