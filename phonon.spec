%define         svn   814039

Name:           phonon
Summary:        KDE4 Multimedia Framework 
Version:        4.2
Release:        %mkrel 0.%{svn}.1
Url:            http://websvn.kde.org/branches/phonon/4.2/
License:        LGPL v2+
Group:          Graphical desktop/KDE
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source0:        %{name}-%{version}.%{svn}.tar.bz2

%description
Phonon is  the KDE4 Multimedia Framework

%files
%defattr(-,root,root)
%{_kde_datadir}/kde4/services/phononbackends/gstreamer.desktop
%{_kde_libdir}/kde4/plugins/phonon_backend/phonon_gstreamer.a

#------------------------------------------------

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

#------------------------------------------------

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

#------------------------------------------------


%package devel
Group: Development/KDE and Qt
Summary: Header files and documentation for compiling KDE applications
Requires: %libphononexperimental = %version
Requires: %libphonon = %version
Requires: %name = %version
Conflicts: kdelibs4-devel < 4.0.80-5

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

#------------------------------------------------

%prep
%setup -q 

%build
%cmake_kde4
%make

%install
cd build
make DESTDIR=%buildroot install

%clean
%{__rm} -rf "%{buildroot}"
