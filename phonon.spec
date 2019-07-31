%define major 4
%define debugcflags %nil
%define debug_package %nil

# (tpg) if disabled then phonon-devel is empty
%bcond_with qt4

Summary:	Plasma Multimedia Framework
Name:		phonon
Version:	4.10.3
Release:	1
Epoch:		2
License:	LGPLv2+
Group:		Graphical desktop/KDE
Url:		http://phonon.kde.org/
Source0:	http://download.kde.org/stable/phonon/%{version}/%{name}-%{version}.tar.xz
Patch0:		phonon-4.6.50-phonon-allow-stop-empty-source.patch
#BuildRequires:	automoc4
BuildRequires:	cmake
BuildRequires:	imagemagick
%if %{with qt4}
# Qt4 old stuff
BuildRequires:	qt4-devel
BuildRequires:	qt4-qmlviewer
%endif
# Qt5 new stuff
BuildRequires:	qmake5
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5OpenGL)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5DBus)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5Quick)
BuildRequires:	pkgconfig(Qt5UiTools)
BuildRequires:	pkgconfig(Qt5Quick)
BuildRequires:	qt5-designer
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	cmake(ECM)
BuildRequires:	ninja

%description
Phonon is the Plasma Multimedia Framework.

%files -f %{name}.lang

#--------------------------------------------------------------------

%define libphonon4qt5experimental %mklibname phonon4qt5experimental %{major}

%package -n %{libphonon4qt5experimental}
Summary:	Phonon Library
Group:		System/Libraries

%description -n %{libphonon4qt5experimental}
Library for Phonon.

%files -n %{libphonon4qt5experimental}
%{_libdir}/libphonon4qt5experimental.so.%{major}*

#--------------------------------------------------------------------

%define libphonon4qt5 %mklibname phonon4qt5 %{major}

%package -n %{libphonon4qt5}
Summary:	Phonon Library
Group:		System/Libraries
# The %{name} package contains only translations
Recommends:	%{name} = %{EVRD}

%description -n %{libphonon4qt5}
Library for Phonon.

%files -n %{libphonon4qt5}
%{_libdir}/libphonon4qt5.so.%{major}*


#--------------------------------------------------------------------
%package -n phonon4qt5-designer-plugin
Summary:	Phonon Designer Plugin
Group:		System/Libraries

%description -n phonon4qt5-designer-plugin
Designer plugin for phonon for Qt 5.

%files -n phonon4qt5-designer-plugin
%{_libdir}/qt5/plugins/designer/phononwidgets.so

#--------------------------------------------------------------------

%package -n phonon4qt5-devel
Group:		Development/KDE and Qt
Summary:	Phonon Development Files
Requires:	%{libphonon4qt5experimental} = %{EVRD}
Requires:	%{libphonon4qt5} = %{EVRD}
Requires:	phonon4qt5-designer-plugin = %{EVRD}

%description -n phonon4qt5-devel
Header files needed to compile applications for KDE.

%files -n phonon4qt5-devel
%{_libdir}/qt5/mkspecs/modules/qt_phonon4qt5.pri
%{_datadir}/dbus-1/interfaces/org.kde.Phonon4Qt5.AudioOutput.xml
%{_datadir}/phonon4qt5/buildsystem/
%{_includedir}/phonon4qt5/
%{_libdir}/libphonon4qt5.so
%{_libdir}/libphonon4qt5experimental.so
%{_libdir}/pkgconfig/phonon4qt5.pc
%{_libdir}/cmake/phonon4qt5

#--------------------------------------------------------------------

%if %{with qt4}
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
%{_libdir}/cmake/phonon

#--------------------------------------------------------------------
%package designer-plugin
Summary:	Phonon Designer Plugin
Group:		System/Libraries
Conflicts:	qt4-designer-plugin-phonon <= 5:4.7.4

%description designer-plugin
Designer plugin for phonon.

%files designer-plugin
%{_qt_plugindir}/designer/libphononwidgets.so

%endif


%prep
%setup -q
%apply_patches

%if %{with qt4}
mkdir Qt4
mv `ls -1 |grep -v Qt4` Qt4
cp -a Qt4 Qt5
%endif

%build
%if %{with qt4}
cd Qt4
%cmake \
	-DCMAKE_BUILD_TYPE:STRING="Release" \
	-DQT_QMAKE_EXECUTABLE=/usr/lib/qt4/bin/qmake \
	-DPHONON_INSTALL_QT_COMPAT_HEADERS:BOOL=ON \
	-DWITH_PulseAudio=ON \
	-DPHONON_INSTALL_QT_EXTENSIONS_INTO_SYSTEM_QT:BOOL=ON

%make
cd ../../Qt5
%endif

%cmake_qt5 \
	-DCMAKE_BUILD_TYPE:STRING="Release" \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-DPHONON_BUILD_PHONON4QT5:BOOL=ON \
	-DWITH_PulseAudio=ON \
	-DPHONON_INSTALL_QT_COMPAT_HEADERS:BOOL=ON \
	-DPHONON_INSTALL_QT_EXTENSIONS_INTO_SYSTEM_QT:BOOL=ON \
	-G Ninja
%ninja_build


%install
%if %{with qt4}
cd Qt4
%makeinstall_std -C build
cd ../Qt5
%endif

%ninja_install -C build

find %{buildroot}%{_datadir}/locale -name "*.qm" |while read r; do
	L=`echo $r |rev |cut -d/ -f3 |rev`
	echo "%%lang($L) %%{_datadir}/locale/$L/LC_MESSAGES/*.qm" >>%{name}.lang
done
