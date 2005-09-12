
%define version 6.3.2
%define release 0.6

#BuildRequires: xorg-util-macros xorg-proto xorg-lib-X11 xorg-lib-Xext xorg-lib-Xt
BuildRequires: xorg-x11-libXxf86vm-devel
BuildRoot: /var/tmp/build-%{name}-%{version}
Group: System Environment/Libraries
License: dunno
Release: %{release}
Source0: MesaLib-%{version}.tar.bz2
# temporary, should be fixed in the next release
Source1: r200_vtxtmp_x86.S
Source2: radeon_vtxtmp_x86.S
Patch0: mesa-6.3.2-compile.patch
Version: %{version}

Name: mesa
Summary: Mesa

%description
Mesa provides a library that may or may not meet the requirements of the OpenGL API.

%package devel
Summary: Libraries and headers needed to build programs using Mesa.
Group: Development/Libraries
%description devel
Libraries and headers needed to build programs using Mesa.

%package dri-ffb
Group: User Interface/X Hardware Support
Summary: DRI driver for ffb
%description dri-ffb
DRI driver for ffb

%package dri-i810
Group: User Interface/X Hardware Support
Summary: DRI driver for i810
%description dri-i810
DRI driver for i810

%package dri-i830
Group: User Interface/X Hardware Support
Summary: DRI driver for i830
%description dri-i830
DRI driver for i830

%package dri-i915
Group: User Interface/X Hardware Support
Summary: DRI driver for i915
%description dri-i915
DRI driver for i915

%package dri-mach64
Group: User Interface/X Hardware Support
Summary: DRI driver for mach64
%description dri-mach64
DRI driver for mach64

%package dri-mga
Group: User Interface/X Hardware Support
Summary: DRI driver for mga
%description dri-mga
DRI driver for mga

%package dri-r128
Group: User Interface/X Hardware Support
Summary: DRI driver for r128
%description dri-r128
DRI driver for r128

%package dri-r200
Group: User Interface/X Hardware Support
Summary: DRI driver for r200
%description dri-r200
DRI driver for r200

%package dri-r300
Group: User Interface/X Hardware Support
Summary: DRI driver for r300
%description dri-r300
DRI driver for r300

%package dri-radeon
Group: User Interface/X Hardware Support
Summary: DRI driver for radeon
%description dri-radeon
DRI driver for radeon

%package dri-s3v
Group: User Interface/X Hardware Support
Summary: DRI driver for s3v
%description dri-s3v
DRI driver for s3v

%package dri-savage
Group: User Interface/X Hardware Support
Summary: DRI driver for savage
%description dri-savage
DRI driver for savage

%package dri-sis
Group: User Interface/X Hardware Support
Summary: DRI driver for sis
%description dri-sis
DRI driver for sis

%package dri-tdfx
Group: User Interface/X Hardware Support
Summary: DRI driver for tdfx
%description dri-tdfx
DRI driver for tdfx

%package dri-trident
Group: User Interface/X Hardware Support
Summary: DRI driver for trident
%description dri-trident
DRI driver for trident

%package dri-unichrome
Group: User Interface/X Hardware Support
Summary: DRI driver for unichrome
%description dri-unichrome
DRI driver for unichrome

%prep
%setup -T -b 0 -n Mesa-%{version}
%patch0 -p1
cp %{SOURCE1} src/mesa/drivers/dri/r200/
cp %{SOURCE2} src/mesa/drivers/dri/radeon/

%build
make linux-dri-x86

%install
#echo -ne "\n\n\n" | make DESTDIR=$RPM_BUILD_ROOT install
mkdir -p %{buildroot}%{_includedir}/GL
cp include/GL/*.h %{buildroot}%{_includedir}/GL/
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_libdir}/dri
cp -a lib/lib* %{buildroot}%{_libdir}/
cp -a lib/*_dri.so %{buildroot}%{_libdir}/dri/

%files
%defattr(-, root, root)
%{_libdir}/lib*.so.*
%dir %{_libdir}/dri

%files devel
%{_includedir}/GL/*
%{_libdir}/lib*.so

%files dri-ffb
%dir %{_libdir}/dri
%{_libdir}/dri/ffb_dri.so

%files dri-i810
%dir %{_libdir}/dri
%{_libdir}/dri/i810_dri.so

%files dri-i830
%dir %{_libdir}/dri
%{_libdir}/dri/i830_dri.so

%files dri-i915
%dir %{_libdir}/dri
%{_libdir}/dri/i915_dri.so

%files dri-mach64
%dir %{_libdir}/dri
%{_libdir}/dri/mach64_dri.so

%files dri-mga
%dir %{_libdir}/dri
%{_libdir}/dri/mga_dri.so

%files dri-r128
%dir %{_libdir}/dri
%{_libdir}/dri/r128_dri.so

%files dri-r200
%dir %{_libdir}/dri
%{_libdir}/dri/r200_dri.so

%files dri-r300
%dir %{_libdir}/dri
%{_libdir}/dri/r300_dri.so

%files dri-radeon
%dir %{_libdir}/dri
%{_libdir}/dri/radeon_dri.so

%files dri-s3v
%dir %{_libdir}/dri
%{_libdir}/dri/s3v_dri.so

%files dri-savage
%dir %{_libdir}/dri
%{_libdir}/dri/savage_dri.so

%files dri-sis
%dir %{_libdir}/dri
%{_libdir}/dri/sis_dri.so

%files dri-tdfx
%dir %{_libdir}/dri
%{_libdir}/dri/tdfx_dri.so

%files dri-trident
%dir %{_libdir}/dri
%{_libdir}/dri/trident_dri.so

%files dri-unichrome
%dir %{_libdir}/dri
%{_libdir}/dri/unichrome_dri.so

%changelog
* Sun Sep 04 2005 Bill Crawford <billcrawford1970@hotmail.com>
- change config to use gcc -M -MF depend

* Sat Sep 03 2005 Bill Crawford <billcrawford1970@hotmail.com>
- split out the -devel package
- split out the dri drivers
- actually remove the dri drivers from the main package

* Tue Aug 23 2005 Bill Crawford <billcrawford1970@hotmail.com>
- added missing files from CVS that were missing from the release
- added patches to get the thing to build and install
- added dri driver modules to file list

* Mon Aug 22 2005 Bill Crawford <billcrawford1970@hotmail.com>
- added BuildRequires
