%define major 4

Summary:	KDE4 Multimedia Framework
Name:		phonon
Version:	4.7.0
Release:	6
Epoch:		2
License:	LGPLv2+
Group:		Graphical desktop/KDE
Url:		http://phonon.kde.org/
Source0:	ftp://ftp.kde.org/pub/kde/stable/phonon/%{version}/%{name}-%{version}.tar.xz
Patch0:		phonon-4.6.50-phonon-allow-stop-empty-source.patch
Patch1:		phonon-4.7.0-cmake.patch
Patch2:		0003-fix-rpath-handling.patch
Patch3:		phonon-4.7.0-qdebug-capturecategory.patch
BuildRequires:	automoc4
BuildRequires:	cmake
BuildRequires:	imagemagick
BuildRequires:	qt4-devel
BuildRequires:	qt4-qmlviewer
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(libpulse)

%description
Phonon is the KDE4 Multimedia Framework.

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

