%define pkgname Mesa

# NOTE: Build target macros:  For now, we will just use build_fc and
# build_rhel to simplify things, until there is a reason to break it
# into per-release macros.  Only 1 of these macros should be enabled.
%define build_fc	1
%define build_rhel	0

#-- DRI Build Configuration ------------------------------------------
# NOTE: Enable DRI on PPC for Fedora Core Mac users, but disable on
# RHEL for improved stability, as DRI isn't really that important
# on server platforms.
%if %{build_fc}
%define with_dri_ppc %{with_dri}
%endif
%if %{build_rhel}
%define with_dri_ppc 0
%endif

# Define arches to make with_dri enabled by default
%ifarch %{ix86} x86_64 ia64 alpha
%define with_dri 1
%endif
# Define PPC OS variant override.
%ifarch ppc
%define with_dri %{with_dri_ppc}
%endif
# Define arches to make with_dri disabled by default
%ifarch ppc64 s390 s390x
%define with_dri 0
%endif

#-- END DRI Build Configuration ------------------------------------------

Summary: Mesa
Name: mesa
Version: 6.3.2
Release: 2
License: MIT/X11
Group: System Environment/Libraries
URL: http://www.mesa3d.org
Source0: MesaLib-%{version}.tar.bz2
# FIXME; Upstream Mesa 6.3.2 as shipped is broken and missing files for
# the linux-dri-x86 target.
Source1: redhat-mesa-target
Source2: redhat-mesa-driver-install
Source10: r200_vtxtmp_x86.S
Source11: radeon_vtxtmp_x86.S
#Patch0: mesa-6.3.2-makedepend.patch
Patch0: mesa-6.3.2-build-configuration-v4.patch
Patch1: mesa-6.3.2-fix-installmesa.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires: libdrm-devel
BuildRequires: libXxf86vm-devel
#BuildRequires: xorg-x11-xtrans-devel

#Provides: %{pkgname}
#Conflicts: XFree86-libs, xorg-x11-libs

%description
Mesa

%package libGL
Summary: Mesa libGL runtime libraries and DRI drivers.
Group: System Environment/Libraries
#Requires: %{name} = %{version}-%{release}

#Provides: %{pkgname}-devel
#Conflicts: XFree86-devel, xorg-x11-devel

%description libGL
Mesa libGL runtime libraries and DRI drivers.

%package libGL-devel
Summary: Mesa libGL development package
Group: Development/Libraries
#Requires: %{name} = %{version}-%{release}

#Provides: %{pkgname}-devel
#Conflicts: XFree86-devel, xorg-x11-devel

%description libGL-devel
Mesa libGL development package

%package libGLU
Summary: Mesa libGLU runtime library
Group: System Environment/Libraries
#Requires: %{name} = %{version}-%{release}

#Provides: %{pkgname}-devel
#Conflicts: XFree86-devel, xorg-x11-devel

%description libGLU
Mesa libGLU runtime library

%package libGLU-devel
Summary: Mesa libGLU development package
Group: Development/Libraries
#Requires: %{name} = %{version}-%{release}

#Provides: %{pkgname}-devel
#Conflicts: XFree86-devel, xorg-x11-devel

%description libGLU-devel
Mesa libGLU development package

%package libGLw
Summary: Mesa libGLw runtime library
Group: System Environment/Libraries
#Requires: %{name} = %{version}-%{release}

#Provides: %{pkgname}-devel
#Conflicts: XFree86-devel, xorg-x11-devel

%description libGLw
Mesa libGLw runtime library

%package libGLw-devel
Summary: Mesa libGLw development package
Group: Development/Libraries
#Requires: %{name} = %{version}-%{release}

#Provides: %{pkgname}-devel
#Conflicts: XFree86-devel, xorg-x11-devel

%description libGLw-devel
Mesa libGLw development package

#---------------------------------------------------------------------
%prep
%setup -q -n Mesa-%{version}
# Copy Red Hat Mesa build/install simplification scripts into build dir.
install -m 755 %{SOURCE1} ./
install -m 755 %{SOURCE2} ./
# FIXME: Install files missing from upstream Mesa 6.3.2 source
cp %{SOURCE10} src/mesa/drivers/dri/r200/
cp %{SOURCE11} src/mesa/drivers/dri/radeon/

#%patch0 -p0 -b .makedepend
%patch1 -p0 -b .fix-installmesa

#---------------------------------------------------------------------
%build
# Macroize this to simplify things
%define makeopts MKDEP="gcc -M" MKDEP_OPTIONS="-MF depend"
# NOTE: We use a custom script to determine which Mesa build target should
# be used, and reduce spec file clutter.
MESATARGET="$(./redhat-mesa-target %{with_dri} %{_arch})"
make ${MESATARGET} %{makeopts}

#---------------------------------------------------------------------
%install
rm -rf $RPM_BUILD_ROOT
#%%makeinstall DESTDIR=$RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/usr

%if %{with_dri}
export DRIMODULEDIR="$RPM_BUILD_ROOT%{_libdir}/dri"
echo $DRIMODULEDIR
./redhat-mesa-driver-install %{_arch}
%endif

# No glut stuff.
rm $RPM_BUILD_ROOT%{_includedir}/GL/uglglutshapes.h
#rm $RPM_BUILD_ROOT%{_includedir}/GL/uglmesa.h

# We intentionally don't ship *.la files
#rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post libGL -p /sbin/ldconfig
%postun libGL -p /sbin/ldconfig
%post libGLU -p /sbin/ldconfig
%postun libGLU -p /sbin/ldconfig
%post libGLw -p /sbin/ldconfig
%postun libGLw -p /sbin/ldconfig

#%%files
#%defattr(-,root,root,-)
#%doc
%files libGL
%defattr(-,root,root,-)
%dir %{_libdir}
%{_libdir}/libGL.so.1
%{_libdir}/libGL.so.1.2
%dir %{_libdir}/dri
# x86 DRI modules
%if %{with_dri}
#%{_libdir}/dri/ffb_dri.so
%{_libdir}/dri/i810_dri.so
%{_libdir}/dri/i830_dri.so
%{_libdir}/dri/i915_dri.so
#%{_libdir}/dri/mach64_dri.so
%{_libdir}/dri/mga_dri.so
%{_libdir}/dri/r128_dri.so
%{_libdir}/dri/r200_dri.so
#%{_libdir}/dri/r300_dri.so
%{_libdir}/dri/radeon_dri.so
#%{_libdir}/dri/s3v_dri.so
%{_libdir}/dri/savage_dri.so
%{_libdir}/dri/sis_dri.so
#%{_libdir}/dri/tdfx_dri.so
#%{_libdir}/dri/trident_dri.so
%{_libdir}/dri/unichrome_dri.so
%endif

%files libGL-devel
%defattr(-,root,root,-)
%{_includedir}/GL/amesa.h
%{_includedir}/GL/directfbgl.h
%{_includedir}/GL/dmesa.h
%{_includedir}/GL/fxmesa.h
%{_includedir}/GL/ggimesa.h
%{_includedir}/GL/gl.h
%{_includedir}/GL/gl_mangle.h
%{_includedir}/GL/glext.h
%{_includedir}/GL/glx.h
%{_includedir}/GL/glx_mangle.h
%{_includedir}/GL/glxext.h
%{_includedir}/GL/mesa_wgl.h
%{_includedir}/GL/mglmesa.h
%{_includedir}/GL/osmesa.h
%{_includedir}/GL/svgamesa.h
#%{_includedir}/GL/uglglutshapes.h
%{_includedir}/GL/uglmesa.h
%{_includedir}/GL/vms_x_fix.h
%{_includedir}/GL/wmesa.h
%{_includedir}/GL/xmesa.h
%{_includedir}/GL/xmesa_x.h
%{_includedir}/GL/xmesa_xf86.h
%{_libdir}/libGL.so

%files libGLU
%defattr(-,root,root,-)
%{_libdir}/libGLU.so.1
%{_libdir}/libGLU.so.1.3.060302

%files libGLU-devel
%defattr(-,root,root,-)
%{_libdir}/libGLU.so
%{_includedir}/GL/glu.h
%{_includedir}/GL/glu_mangle.h

%files libGLw
%defattr(-,root,root,-)
%{_libdir}/libGLw.so.1
%{_libdir}/libGLw.so.1.0.0

%files libGLw-devel
%defattr(-,root,root,-)
%{_libdir}/libGLw.so

%changelog
* Sun Sep 4 2005 Mike A. Harris <mharris@redhat.com> 6.3.2-1
- Initial build.
