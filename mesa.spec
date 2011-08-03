# S390 doesn't have video cards, but we need swrast for xserver's GLX
%ifarch s390 s390x
%define with_hardware 0
%define dri_drivers --with-dri-drivers=swrast
%else
%define with_hardware 1
%define base_drivers mga,nouveau,r128,radeon,r200,savage,tdfx
%ifarch %{ix86}
%define ix86_drivers ,i810,i915,i965,sis,unichrome
%endif
%ifarch x86_64
%define amd64_drivers ,i915,i965,unichrome
%endif
%ifarch ia64
%define ia64_drivers ,i915
%endif
%define dri_drivers --with-dri-drivers=%{base_drivers}%{?ix86_drivers}%{?amd64_drivers}%{?ia64_drivers}
%endif

%define _default_patch_fuzz 2

%define manpages gl-manpages-1.0.1
#define gitdate 20110730
#% define snapshot 

Summary: Mesa graphics libraries
Name: mesa
Version: 7.11
Release: 2%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.mesa3d.org

#Source0: http://downloads.sf.net/mesa3d/MesaLib-%{version}.tar.bz2
#Source0: http://www.mesa3d.org/beta/MesaLib-%{version}%{?snapshot}.tar.bz2
Source0: ftp://ftp.freedesktop.org/pub/%{name}/%{version}/MesaLib-%{version}.tar.bz2
#Source0: %{name}-%{gitdate}.tar.xz
Source2: %{manpages}.tar.bz2
Source3: make-git-snapshot.sh

Patch2: mesa-7.1-nukeglthread-debug.patch
Patch3: mesa-no-mach64.patch
Patch4: legacy-drivers.patch

#Patch7: mesa-7.1-link-shared.patch
Patch8: mesa-7.10-llvmcore.patch

Patch30: mesa-7.6-hush-vblank-warning.patch
Patch31: mesa-7.10-swrastg.patch

BuildRequires: pkgconfig autoconf automake libtool
%if %{with_hardware}
BuildRequires: kernel-headers >= 2.6.27-0.305.rc5.git6
BuildRequires: xorg-x11-server-devel
%endif
BuildRequires: libdrm-devel >= 2.4.24-1
BuildRequires: libXxf86vm-devel
BuildRequires: expat-devel >= 2.0
BuildRequires: xorg-x11-proto-devel >= 7.4-35
BuildRequires: makedepend
BuildRequires: libselinux-devel
BuildRequires: libXext-devel
BuildRequires: libXfixes-devel
BuildRequires: libXdamage-devel
BuildRequires: libXi-devel
BuildRequires: libXmu-devel
BuildRequires: elfutils
BuildRequires: python
BuildRequires: llvm-static
BuildRequires: libxml2-python
BuildRequires: libudev-devel
BuildRequires: libtalloc-devel
BuildRequires: bison flex

%description
Mesa

%package libGL
Summary: Mesa libGL runtime libraries and DRI drivers
Group: System Environment/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Provides: libGL
Requires: libdrm%{?isa} >= 2.4.23-1
%if %{with_hardware}
Conflicts: xorg-x11-server-Xorg < 1.4.99.901-14
%endif

%description libGL
Mesa libGL runtime library.

%package libEGL
Summary: Mesa libEGL runtime libraries
Group: System Environment/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires: mesa-dri-drivers%{?_isa} = %{version}-%{release}
Requires: libdrm%{?isa} >= 2.4.23-1

%description libEGL
Mesa libEGL runtime libraries

%package libGLES
Summary: Mesa libGLES runtime libraries
Group: System Environment/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires: mesa-dri-drivers%{?_isa} = %{version}-%{release}
Requires: libdrm%{?isa} >= 2.4.23-1

%description libGLES
Mesa GLES runtime libraries

%package dri-filesystem
Summary: Mesa DRI driver filesystem
Group: User Interface/X Hardware Support
%description dri-filesystem
Mesa DRI driver filesystem

%package dri-drivers
Summary: Mesa-based DRI drivers
Group: User Interface/X Hardware Support
Requires: mesa-dri-filesystem%{?_isa}
Obsoletes: mesa-dri-drivers-experimental < 0:7.10-0.24
Obsoletes: mesa-dri-llvmcore <= 7.11-0.8
%description dri-drivers
Mesa-based DRI drivers.

%package dri-drivers-dri1
Summary: Mesa-based DRI1 drivers
Group: User Interface/X Hardware Support
Requires: mesa-dri-filesystem%{?isa}
%description dri-drivers-dri1
Mesa-based DRI1 drivers.

%package libGL-devel
Summary: Mesa libGL development package
Group: Development/Libraries
Requires: mesa-libGL = %{version}-%{release}
Provides: libGL-devel
Conflicts: xorg-x11-proto-devel <= 7.2-12

%description libGL-devel
Mesa libGL development package

%package libEGL-devel
Summary: Mesa libEGL development package
Group: Development/Libraries
Requires: mesa-libEGL = %{version}-%{release}

%description libEGL-devel
Mesa libEGL development package

%package libGLES-devel
Summary: Mesa libGLES development package
Group: Development/Libraries
Requires: mesa-libGLES = %{version}-%{release}

%description libGLES-devel
Mesa libGLES development package

%package libGLU
Summary: Mesa libGLU runtime library
Group: System Environment/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Provides: libGLU

%description libGLU
Mesa libGLU runtime library


%package libGLU-devel
Summary: Mesa libGLU development package
Group: Development/Libraries
Requires: mesa-libGLU = %{version}-%{release}
Provides: libGLU-devel

%description libGLU-devel
Mesa libGLU development package


%package libOSMesa
Summary: Mesa offscreen rendering libraries
Group: System Environment/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Provides: libOSMesa

%description libOSMesa
Mesa offscreen rendering libraries


%package libOSMesa-devel
Summary: Mesa offscreen rendering development package
Group: Development/Libraries
Requires: mesa-libOSMesa = %{version}-%{release}

%description libOSMesa-devel
Mesa offscreen rendering development package


%prep
%setup -q -n Mesa-%{version}%{?snapshot} -b0 -b2
#setup -q -n mesa-%{gitdate} -b2
%patch2 -p1 -b .intel-glthread
%patch3 -p1 -b .no-mach64
%patch4 -p1 -b .classic
#patch7 -p1 -b .dricore
%patch8 -p1 -b .llvmcore
%patch30 -p1 -b .vblank-warning
#patch31 -p1 -b .swrastg

%build

autoreconf --install  

export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"
%ifarch %{ix86}
# i do not have words for how much the assembly dispatch code infuriates me
%define common_flags --enable-selinux --enable-pic --disable-asm
%else
%define common_flags --enable-selinux --enable-pic
%endif

%configure %{common_flags} \
    --disable-glw \
    --disable-glut \
    --enable-gl-osmesa \
    --with-driver=dri \
    --with-osmesa-bits=8 \
    --with-dri-driverdir=%{_libdir}/dri \
    --enable-egl \
    --enable-gles1 \
    --enable-gles2 \
    --disable-gallium-egl \
%if %{with_hardware}
    --with-gallium-drivers=r300,r600,nouveau,swrast \
    --enable-gallium-llvm \
%else
    --disable-gallium-llvm \
    --with-gallium-drivers=swrast \
%endif
    %{?dri_drivers}

make %{?_smp_mflags}

pushd ../%{manpages}
autoreconf -v --install
%configure
make %{?_smp_mflags}
popd

%install
rm -rf $RPM_BUILD_ROOT

# core libs and headers, but not drivers.
make install DESTDIR=$RPM_BUILD_ROOT DRI_DIRS=

# just the DRI drivers that are sane
install -d $RPM_BUILD_ROOT%{_libdir}/dri
# use gallium driver iff built
[ -f %{_lib}/gallium/r300_dri.so ] && cp %{_lib}/gallium/r300_dri.so %{_lib}/r300_dri.so
[ -f %{_lib}/gallium/r600_dri.so ] && cp %{_lib}/gallium/r600_dri.so %{_lib}/r600_dri.so
[ -f %{_lib}/gallium/swrastg_dri.so ] && mv %{_lib}/gallium/swrastg_dri.so %{_lib}/swrast_dri.so

for f in i810 i915 i965 mach64 mga r128 r200 r300 r600 radeon savage sis swrast tdfx unichrome nouveau_vieux gallium/vmwgfx ; do
    so=%{_lib}/${f}_dri.so
    test -e $so && echo $so
done | xargs install -m 0755 -t $RPM_BUILD_ROOT%{_libdir}/dri >& /dev/null || :

# strip out undesirable headers
pushd $RPM_BUILD_ROOT%{_includedir}/GL 
rm -f [a-fh-np-wyz]*.h glf*.h glut*.h
popd

pushd $RPM_BUILD_ROOT%{_libdir}
rm -f xorg/modules/drivers/modesetting_drv.so
popd

# man pages
pushd ../%{manpages}
make %{?_smp_mflags} install DESTDIR=$RPM_BUILD_ROOT
popd

# this keeps breaking, check it early.  note that the exit from eu-ftr is odd.
pushd $RPM_BUILD_ROOT%{_libdir}
for i in libOSMesa*.so libGL.so ; do
    eu-findtextrel $i && exit 1
done
popd

%clean
rm -rf $RPM_BUILD_ROOT

%check

%post libGL -p /sbin/ldconfig
%postun libGL -p /sbin/ldconfig
%post libGLU -p /sbin/ldconfig
%postun libGLU -p /sbin/ldconfig
%post libOSMesa -p /sbin/ldconfig
%postun libOSMesa -p /sbin/ldconfig
%post libEGL -p /sbin/ldconfig
%postun libEGL -p /sbin/ldconfig
%post libGLES -p /sbin/ldconfig
%postun libGLES -p /sbin/ldconfig

%files libGL
%defattr(-,root,root,-)
%doc docs/COPYING
%{_libdir}/libGL.so.1
%{_libdir}/libGL.so.1.*

%files libEGL
%defattr(-,root,root,-)
%doc docs/COPYING
%{_libdir}/libEGL.so.1
%{_libdir}/libEGL.so.1.*

%files libGLES
%defattr(-,root,root,-)
%doc docs/COPYING
%{_libdir}/libGLESv1_CM.so.1
%{_libdir}/libGLESv1_CM.so.1.*
%{_libdir}/libGLESv2.so.2
%{_libdir}/libGLESv2.so.2.*
%{_libdir}/libglapi.so.0
%{_libdir}/libglapi.so.0.*

%files dri-filesystem
%defattr(-,root,root,-)
%doc docs/COPYING
%dir %{_libdir}/dri

%files dri-drivers
%defattr(-,root,root,-)
%if %{with_hardware}
%{_libdir}/dri/radeon_dri.so
%{_libdir}/dri/r200_dri.so
%{_libdir}/dri/r300_dri.so
%{_libdir}/dri/r600_dri.so
%ifarch %{ix86} x86_64 ia64
%{_libdir}/dri/i915_dri.so
%ifnarch ia64
%{_libdir}/dri/i965_dri.so
%endif
%endif
%{_libdir}/dri/nouveau_dri.so
%{_libdir}/dri/nouveau_vieux_dri.so
%endif
%{_libdir}/dri/swrast_dri.so
%exclude %{_libdir}/dri/swrastg_dri.so

%files dri-drivers-dri1
%defattr(-,root,root,-)
%doc docs/COPYING
%if %{with_hardware}
%ifarch %{ix86} x86_64
%{_libdir}/dri/unichrome_dri.so
%ifarch %{ix86}
%{_libdir}/dri/i810_dri.so
%{_libdir}/dri/sis_dri.so
%endif
%endif
%{_libdir}/dri/r128_dri.so
%{_libdir}/dri/mga_dri.so
%{_libdir}/dri/savage_dri.so
%{_libdir}/dri/tdfx_dri.so
%endif

%files libGL-devel
%defattr(-,root,root,-)
%{_includedir}/GL/gl.h
%{_includedir}/GL/gl_mangle.h
%{_includedir}/GL/glext.h
%{_includedir}/GL/glx.h
%{_includedir}/GL/glx_mangle.h
%{_includedir}/GL/glxext.h
%dir %{_includedir}/GL/internal
%{_includedir}/GL/internal/dri_interface.h
%{_libdir}/pkgconfig/dri.pc
%{_libdir}/libGL.so
%{_libdir}/pkgconfig/gl.pc
%{_datadir}/man/man3/gl[^uX]*.3gl*
%{_datadir}/man/man3/glX*.3gl*

%files libEGL-devel
%defattr(-,root,root,-)
%dir %{_includedir}/EGL
%{_includedir}/EGL/eglext.h
%{_includedir}/EGL/egl.h
%{_includedir}/EGL/eglplatform.h
%dir %{_includedir}/KHR
%{_includedir}/KHR/khrplatform.h
%{_libdir}/pkgconfig/egl.pc
%{_libdir}/libEGL.so

%files libGLES-devel
%defattr(-,root,root,-)
%dir %{_includedir}/GLES
%{_includedir}/GLES/egl.h
%{_includedir}/GLES/gl.h
%{_includedir}/GLES/glext.h
%{_includedir}/GLES/glplatform.h
%dir %{_includedir}/GLES2
%{_includedir}/GLES2/gl2platform.h
%{_includedir}/GLES2/gl2.h
%{_includedir}/GLES2/gl2ext.h
%{_libdir}/pkgconfig/glesv1_cm.pc
%{_libdir}/pkgconfig/glesv2.pc
%{_libdir}/libGLESv1_CM.so
%{_libdir}/libGLESv2.so
%{_libdir}/libglapi.so

%files libGLU
%defattr(-,root,root,-)
%{_libdir}/libGLU.so.1
%{_libdir}/libGLU.so.1.3.*

%files libGLU-devel
%defattr(-,root,root,-)
%{_libdir}/libGLU.so
%{_libdir}/pkgconfig/glu.pc
%{_includedir}/GL/glu.h
%{_includedir}/GL/glu_mangle.h
%{_datadir}/man/man3/glu*.3gl*

%files libOSMesa
%defattr(-,root,root,-)
%doc docs/COPYING
%{_libdir}/libOSMesa.so.7*

%files libOSMesa-devel
%defattr(-,root,root,-)
%dir %{_includedir}/GL
%{_includedir}/GL/osmesa.h
%{_libdir}/libOSMesa.so
%{_libdir}/pkgconfig/osmesa.pc

%changelog
* Wed Aug  3 2011 Michel Salim <salimma@fedoraproject.org> - 7.11-2
- Rebuild against final LLVM 2.9 release

* Tue Aug 02 2011 Adam Jackson <ajax@redhat.com> 7.11-1
- Mesa 7.11
- Redo the driver arch exclusion, yet again.  Dear secondary arches: unless
  it's an on-motherboard driver like i915, all PCI drivers are to be built
  for all PCI arches.

* Sat Jul 30 2011 Dave Airlie <airlied@redhat.com> 7.11-0.18.20110730.0
- rebase to latest upstream snapshot (same as F15)

* Thu Jul 07 2011 Peter Lemenkov <lemenkov@gmail.com> - 7.11-0.16.20110620.0
- Fix building on ppc (some dri1 drivers are missing)

* Wed Jul  6 2011 Ville Skyttä <ville.skytta@iki.fi> - 7.11-0.15.20110620.0
- More include dir ownership fixes (#682357).

* Tue Jul 05 2011 Adam Jackson <ajax@redhat.com> 7.11-0.14.20110620.0
- Arch-dep and file ownership fixes (#682357)

* Mon Jun 20 2011 Dave Airlie <airlied@redhat.com> 7.11-0.13.20110620.0
- rebase to 20 June snapshot from upstream - new gallium config options

* Mon Jun 20 2011 Dave Airlie <airlied@redhat.com> 7.11-0.12.20110412.0
- dropping DRI1 is premature, fix swrastg upstream first.

* Tue May 10 2011 Dan Horák <dan[at]danny.cz> 7.11-0.11.20110412.0
- r300 needs to be explicitely disabled when with_hardware == 0

* Mon May 09 2011 Adam Jackson <ajax@redhat.com> 7.11-0.10.20110412.0
- Drop the separate build pass for osmesa, no longer needed.

* Mon May 09 2011 Adam Jackson <ajax@redhat.com> 7.11-0.9.20110412.0
- Drop dri1 subpackage (and its drivers), use "swrastg" consistently.

* Mon May 09 2011 Adam Jackson <ajax@redhat.com> 7.11-0.8.20110412.0
- Use llvm-libs' shared lib instead of rolling our own.

* Mon Apr 18 2011 Adam Jackson <ajax@redhat.com> 7.11-0.7.20110412.0
- Fix intel driver exclusion to be better arched (#697555)

* Tue Apr 12 2011 Dave Airlie <airlied@redhat.com> 7.11-0.6.20110412.0
- latest upstream snapshot to fix r200 regression.

* Fri Apr 01 2011 Dave Airlie <airlied@redhat.com> 7.11-0.5.20110401.0
- Revert upstream patches causing SNB regression.

* Fri Apr 01 2011 Dave Airlie <airlied@redhat.com> 7.11-0.4.20110401.0
- upstream snapshot again - proper fix for ILK + nv50 gnome-shell issue

* Wed Mar 30 2011 Dave Airlie <airlied@redhat.com> 7.11-0.3.20110330.0
- mesa-intel-fix-gs-rendering-regression.patch, attempt to fix gnome shell
  rendering.

* Wed Mar 30 2011 Dave Airlie <airlied@redhat.com> 7.11-0.2.20110330.0
- snapshot upstream again to hopefully fix ILK bug

* Sun Mar 27 2011 Dave Airlie <airlied@redhat.com> 7.11-0.1.20110327.0
- pull latest snapshot + 3 post snapshot fixes

* Wed Mar 23 2011 Adam Jackson <ajax@redhat.com> 7.10.1-1
- mesa 7.10.1

* Fri Mar 18 2011 Dennis Gilmore <dennis@ausil.us> 7.10-0.30
- fall back to non native jit on sparc.

* Mon Mar 14 2011 Dave Airlie <airlied@redhat.com> 7.10-0.29
- use g++ to link llvmcore.so so it gets libstdc++ (#674079)

* Fri Mar 04 2011 Dan Horák <dan[at]danny.cz> 7.10-0.28
- enable gallium-llvm only when with_hardware is set (workarounds linking
  failure on s390(x))

* Wed Feb 23 2011 Jerome Glisse <jglisse@redhat.com> 7.10-0.27
- Build without -fno-omit-frame-pointer as gcc 4.6.0 seems to lead to
  bogus code with that option (#679924)

* Wed Feb 09 2011 Adam Jackson <ajax@redhat.com> 7.10-0.26
- BuildRequires: libdrm >= 2.4.24-0 (#668363)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.10-0.25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 20 2011 Ben Skeggs <bskeggs@redhat.com> 7.10-0.24
- nouveau: move out of -experimental

* Thu Jan 20 2011 Ben Skeggs <bskeggs@redhat.com> 7.10-0.23
- nouveau: nvc0 (fermi) backport + nv10/nv20 gnome-shell fixes

* Tue Jan 18 2011 Adam Jackson <ajax@redhat.com> 7.10-0.22
- Add -dri-filesystem common subpackage for directory and COPYING
- Add -dri-llvmcore subpackage and buildsystem hack

* Tue Jan 18 2011 Adam Jackson <ajax@redhat.com> 7.10-0.21
- Fix the s390 case a different way
- s/i686/%%{ix86}
- Add libudev support for wayland (Casey Dahlin)

* Tue Jan 18 2011 Dan Horák <dan[at]danny.cz> 7.10-0.20
- updated for s390(x), r300 is really built even when with_hardware == 0

* Tue Jan 18 2011 Dave Airlie <airlied@redhat.com> 7.10-0.19
- split out DRI1 drivers to reduce package size.

* Fri Jan 07 2011 Dave Airlie <airlied@redhat.com> 7.10-0.18
- new snapshot from 7.10 branch (include Radeon HD6xxx support)

* Thu Dec 16 2010 Dave Airlie <airlied@redhat.com> 7.10-0.17
- new snapshot from 7.10 branch

* Wed Dec 15 2010 Adam Jackson <ajax@redhat.com> 7.10-0.16
- Today's (yesterday's) git snap.
- Switch the sourceball to xz.

* Mon Dec 06 2010 Adam Jackson <ajax@redhat.com> 7.10-0.15
- Really disable gallium EGL.  Requires disabling OpenVG due to buildsystem
  nonsense.  Someone fix that someday. (Patch from krh)

* Thu Dec 02 2010 Adam Jackson <ajax@redhat.com> 7.10-0.14
- --disable-gallium-egl

* Wed Dec 01 2010 Dan Horák <dan[at]danny.cz> 7.10-0.13
- workaround failing build on s390(x)

* Mon Nov 29 2010 Adam Jackson <ajax@redhat.com> 7.10-0.12
- Today's git snap.

* Thu Nov 18 2010 Adam Jackson <ajax@redhat.com> 7.10-0.11
- Today's git snap.
- Build with -fno-omit-frame-pointer for profiling.
- Install swrastg as the swrast driver.
- legacy-drivers.patch: Disable swrast classic.

* Mon Nov 15 2010 Adam Jackson <ajax@redhat.com>
- Drop Requires: mesa-dri-drivers from -experimental, not needed in a non-
  dricore build.
- Drop Requires: mesa-dri-drivers from -libGL, let comps do that.

* Thu Nov 11 2010 Adam Jackson <ajax@redhat.com> 7.10-0.10
- Build libOpenVG too
- Add X driver ABI magic for vmwgfx
- Linker script hack for swrastg to make it slightly less offensively huge

* Mon Nov 08 2010 Dave Airlie <airlied@redhat.com> 7.10-0.9
- update to latest git snap + enable r600g by default

* Sat Nov 06 2010 Dave Airlie <airlied@redhat.com> 7.10-0.8
- enable EGL/GLES

* Wed Nov 03 2010 Dave Airlie <airlied@redhat.com> 7.10-0.7
- fix r300g selection

* Tue Nov 02 2010 Adam Jackson <ajax@redhat.com> 7.10-0.6
- Use standard CFLAGS
- Move swrastg_dri to -experimental

* Mon Nov 01 2010 Adam Jackson <ajax@redhat.com> 7.10-0.5
- BR: llvm-static not llvm-devel (#627965)

* Thu Oct 28 2010 Adam Jackson <ajax@redhat.com> 7.10-0.4
- -dri-drivers-experimental Requires dri-drivers (#556789)

* Thu Oct 28 2010 Adam Jackson <ajax@redhat.com> 7.10-0.3
- Drop demos and glx-utils subpackages, they have their own source package
  now. (#605719)

* Wed Oct 20 2010 Adam Jackson <ajax@redhat.com> 7.10-0.2
- git snapshot, fixes osmesa linking issues

* Wed Oct 20 2010 Adam Jackson <ajax@redhat.com> 7.10-0.1
- git snapshot
- Drop osmesa16 and osmesa32, nothing's using them

* Tue Aug 24 2010 Dave Airlie <airlied@redhat.com> 7.9-0.7
- latest git snapshot - enable talloc/llvm links

* Tue Jul 20 2010 Dave Airlie <airlied@redhat.com> 7.9-0.6
- snapshot latest git

* Fri Jul 09 2010 Dave Airlie <airlied@redhat.com> 7.9-0.5
- resnapshot latest git

* Thu Jul 08 2010 Adam Jackson <ajax@redhat.com> 7.9-0.4
- Install COPYING like we ought to.

* Thu Jun 24 2010 Dan Horák <dan[at]danny.cz> 7.9-0.3
- add libtool (needed by mesa-demos) to BR: - normally it's brought via
    xorg-x11-util-macros and xorg-x11-server-devel, but not on platforms
    without hardware drivers
- build gallium drivers and the dri-drivers-experimental subpackage only
    when hardware drivers are requested

* Sat Jun 12 2010 Dave Airlie <airlied@redhat.com> 7.9-0.2
- rebase to git snapshot with TFP fixes for r300 + gallium - enable r300g

* Sun May 30 2010 Dave Airlie <airlied@redhat.com> 7.9-0.1
- rebase to a git snapshot - disable vmwgfx

* Mon Feb 08 2010 Ben Skeggs <bskeggs@redhat.com> 7.8-0.16
- patch mesa to enable legacy nouveau driver build on i386

* Mon Feb 08 2010 Ben Skeggs <bskeggs@redhat.com> 7.8-0.15
- rebase for legacy nouveau drivers

* Thu Feb 04 2010 Dave Airlie <airlied@redhat.com> 7.8-0.14
- rebase again to fix r300

* Wed Feb 03 2010 Dave Airlie <airlied@redhat.com> 7.8-0.13
- update dri2proto requirement
- add nouveau to experimental drivers set

* Wed Jan 27 2010 Dave Airlie <airlied@redhat.com> 7.8-0.12
- Fix radeon colors for rawhide

* Thu Jan 21 2010 Dave Airlie <airlied@redhat.com> 7.8-0.11
- rebase for new DRI2 API

* Fri Jan 08 2010 Dave Airlie <airlied@redhat.com> 7.8-0.10
- rebase to new snapshot with fix for radeon in it

* Thu Jan 07 2010 Dave Airlie <airlied@redhat.com> 7.8-0.9
- Disable dricore for now as it conflicts with upstream vis changes

* Wed Jan 06 2010 Dave Airlie <airlied@redhat.com> 7.8-0.8
- update to latest snapshot and fixup build
