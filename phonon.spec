%define major 4

Summary:	Plasma Multimedia Framework
Name:		phonon
Version:	4.12.0
Release:	1
Epoch:		2
License:	LGPLv2+
Group:		Graphical desktop/KDE
Url:		http://phonon.kde.org/
Source0:	http://download.kde.org/stable/phonon/%{version}/%{name}-%{version}.tar.xz
#Patch0:		phonon-4.11.1-clang16-gcc13.patch
BuildRequires:	imagemagick
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


%description
Phonon is the Plasma Multimedia Framework.

%files -f %{name}.lang
%{_bindir}/phononsettings

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
# The %{name} package contains only translations and the phononsettings tool
Requires:	%{name} = %{EVRD}

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
%{_datadir}/phonon4qt5/buildsystem/
%{_includedir}/phonon4qt5/
%{_libdir}/libphonon4qt5.so
%{_libdir}/libphonon4qt5experimental.so
%{_libdir}/pkgconfig/phonon4qt5.pc
%{_libdir}/cmake/phonon4qt5

#--------------------------------------------------------------------

%prep
%autosetup -p1

%build
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
%ninja_install -C build

find %{buildroot}%{_datadir}/locale -name "*.qm" |while read r; do
    L=$(echo $r |rev |cut -d/ -f3 |rev)
    echo "%%lang($L) %%{_datadir}/locale/$L/LC_MESSAGES/$(basename $r)" >>%{name}.lang
done
