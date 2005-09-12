%define pkgname Mesa

%ifarch %{ix86} x86_64 ppc ia64
%define with_dri 1
%else
%define with_dri 0
%endif

Summary: Mesa
Name: mesa
Version: 6.3.2
Release: 1
License: MIT/X11
Group: System Environment/Libraries
URL: http://www.mesa3d.org
Source0: MesaLib-%{version}.tar.bz2
# FIXME; Upstream Mesa 6.3.2 as shipped is broken and missing files for
# the linux-dri-x86 target.
Source1: r200_vtxtmp_x86.S
Source2: radeon_vtxtmp_x86.S
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


%prep
%setup -q -n Mesa-%{version}
cp %{SOURCE1} src/mesa/drivers/dri/r200/
cp %{SOURCE2} src/mesa/drivers/dri/radeon/

#%patch0 -p0 -b .makedepend
%patch1 -p0 -b .fix-installmesa

%build
#%%define makeopts MKDEP="$(which makedepend)"
%define makeopts MKDEP="gcc -M -MF depend" MKDEP_OPTIONS=

#export MKDEP="$(which makedepend)"
%ifarch %{ix86}
make linux-dri-x86 %{makeopts}
%endif

%ifarch x86_64
make linux-dri-x86_64 %{makeopts}
%endif

# FIXME: ppc DRI needs to be Fedora Core only!  Not for RHEL!
%ifarch ppc
# With DRI
make linux-dri-ppc %{makeopts}
%else
# Without DRI
make linux-ppc %{makeopts}
%endif

%ifarch ia64 alpha
make linux-dri %{makeopts}
%endif

%ifarch ppc64 s390 s390x sparc sparc64
make linux %{makeopts}
%endif

%install
rm -rf $RPM_BUILD_ROOT
#cd %{pkgname}-%{version}
#%%makeinstall DESTDIR=$RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/usr

%if %{with_dri}
# FIXME: FC5's current kernel has the following DRM modules.  Some of them
# shouldn't be there at all (ppc64), some don't make much sense (via on
# ppc).  We'll have to talk to kernel folk to get the ones disabled that
# don't make sense, or which we don't want to ship for some reason or
# another.
#
# for a in i586 i686 ia64 ppc ppc64 s390x x86_64 ; do (echo -n "${a}:" \
# rpm -qlp /mnt/redhat/beehive/comps/dist/fc5/kernel/2.6.13-1.1536_FC5/$a/kernel-2.6.13-1.1536_FC5.$a.rpm | \
# grep /drm/ | sed -e 's;.*/;;g' |xargs echo ) ;done
#
# i586:  drm.ko i810.ko i830.ko i915.ko mga.ko r128.ko radeon.ko savage.ko sis.ko tdfx.ko via.ko
# i686:  drm.ko i810.ko i830.ko i915.ko mga.ko r128.ko radeon.ko savage.ko sis.ko tdfx.ko via.ko
# ia64:  drm.ko mga.ko r128.ko radeon.ko savage.ko sis.ko tdfx.ko via.ko
# ppc:   drm.ko mga.ko r128.ko radeon.ko savage.ko sis.ko tdfx.ko via.ko
# ppc64: drm.ko mga.ko r128.ko radeon.ko savage.ko sis.ko tdfx.ko via.ko
# s390x:
# x86_64: drm.ko i810.ko i830.ko i915.ko mga.ko r128.ko radeon.ko savage.ko sis.ko tdfx.ko via.ko

%define alldridrivers ffb i810 i830 i915 mach64 mga r128 r200 r300 radeon s3v savage sis tdfx trident unichrome
%ifarch %{ix86}
%define dridrivers i810 i830 i915 mga r128 r200 radeon savage sis unichrome
%endif
%ifarch x86_64
%define dridrivers i810 i830 i915 mga r128 r200 radeon savage sis unichrome
%endif
%ifarch ia64
%define dridrivers mga r128 r200 radeon savage sis
%endif
%if %{with_dri}
%define ppcdridrivers mga r128 r200 radeon
%else
%define ppcdridrivers
%endif
%ifarch ppc
%define dridrivers %{ppcdridrivers}
%endif
%ifarch ppc64 s390 s390x sparc sparc64
%define dridrivers
%endif

# Install DRI drivers
%if %{with_dri}
{
    mkdir -p $RPM_BUILD_ROOT%{_libdir}/dri
    for driver in %{dridrivers} ; do
        install -m 0444 cp -a lib/${driver}_dri.so $RPM_BUILD_ROOT%{_libdir}/dri/
    done
}
%endif

# No glut stuff.
rm $RPM_BUILD_ROOT%{_includedir}/GL/uglglutshapes.h
rm $RPM_BUILD_ROOT%{_includedir}/GL/uglmesa.h

# We intentionally don't ship *.la files
#rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

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
#%{_includedir}/GL/uglmesa.h
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
