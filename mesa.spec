%if 0%{?rhel}
%define with_private_llvm 1
%else
%define with_private_llvm 0
%define with_wayland 1
%endif

# f17 support wayland 0.85, llvm 3.0 means no radeonsi
%if 0%{?fedora} < 18
%define min_wayland_version 0.85
%else
%define min_wayland_version 1.0
%define with_radeonsi 1
%endif

# S390 doesn't have video cards, but we need swrast for xserver's GLX
%ifarch s390 s390x
%define with_hardware 0
%define dri_drivers --with-dri-drivers=
%else
%define with_hardware 1
%define base_drivers nouveau,radeon,r200
%ifarch %{ix86}
%define platform_drivers ,i915,i965
%define with_vmware 1
%endif
%ifarch x86_64
%define platform_drivers ,i915,i965
%define with_vmware 1
%endif
%define dri_drivers --with-dri-drivers=%{base_drivers}%{?platform_drivers}
%endif

%define _default_patch_fuzz 2

%define gitdate 20130508
#% define snapshot 

Summary: Mesa graphics libraries
Name: mesa
Version: 9.2
Release: 0.1.%{gitdate}%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.mesa3d.org

#Source0: http://www.mesa3d.org/beta/MesaLib-%{version}%{?snapshot}.tar.bz2
#Source0: ftp://ftp.freedesktop.org/pub/%{name}/%{version}/MesaLib-%{version}.tar.bz2
# Source0: MesaLib-%{version}.tar.xz
Source0: %{name}-%{gitdate}.tar.xz
Source1: sanitize-tarball.sh
Source2: make-release-tarball.sh
Source3: make-git-snapshot.sh

# src/gallium/auxiliary/postprocess/pp_mlaa* have an ... interestingly worded license.
# Source4 contains email correspondence clarifying the license terms.
# Fedora opts to ignore the optional part of clause 2 and treat that code as 2 clause BSD.
Source4: Mesa-MLAA-License-Clarification-Email.txt

# git diff-tree -p mesa-9.1..origin/9.1 > `git describe origin/9.1`.patch
Patch0: mesa-9.1.1-53-g3cff41c.patch

Patch1: nv50-fix-build.patch
Patch9: mesa-8.0-llvmpipe-shmget.patch
Patch12: mesa-8.0.1-fix-16bpp.patch
Patch14: i965-hack-hiz-snb-fix.patch
Patch15: mesa-9.2-hardware-float.patch
Patch16: mesa-9.2-no-useless-vdpau.patch
# this is suboptimal, or so dave says:
# http://lists.freedesktop.org/archives/mesa-dev/2013-May/039169.html
Patch17: 0001-mesa-Be-less-casual-about-texture-formats-in-st_fina.patch
Patch18: mesa-9.2-llvmpipe-on-big-endian.patch

BuildRequires: pkgconfig autoconf automake libtool
%if %{with_hardware}
BuildRequires: kernel-headers
BuildRequires: xorg-x11-server-devel
%endif
BuildRequires: libdrm-devel >= 2.4.42
BuildRequires: libXxf86vm-devel
BuildRequires: expat-devel
BuildRequires: xorg-x11-proto-devel
BuildRequires: makedepend
BuildRequires: libselinux-devel
BuildRequires: libXext-devel
BuildRequires: libXfixes-devel
BuildRequires: libXdamage-devel
BuildRequires: libXi-devel
BuildRequires: libXmu-devel
BuildRequires: elfutils
BuildRequires: python
BuildRequires: gettext
%if 0%{?with_private_llvm}
BuildRequires: mesa-private-llvm-devel
%else
BuildRequires: llvm-devel >= 3.0
%endif
BuildRequires: elfutils-libelf-devel
BuildRequires: libxml2-python
BuildRequires: libudev-devel
BuildRequires: bison flex
%if !0%{?rhel}
BuildRequires: pkgconfig(wayland-client) >= %{min_wayland_version}
BuildRequires: pkgconfig(wayland-server) >= %{min_wayland_version}
%endif
BuildRequires: mesa-libGL-devel
BuildRequires: libvdpau-devel
BuildRequires: zlib-devel

%description
Mesa

%package libGL
Summary: Mesa libGL runtime libraries and DRI drivers
Group: System Environment/Libraries
Provides: libGL

%description libGL
Mesa libGL runtime library.

%package libEGL
Summary: Mesa libEGL runtime libraries
Group: System Environment/Libraries

%description libEGL
Mesa libEGL runtime libraries

%package libGLES
Summary: Mesa libGLES runtime libraries
Group: System Environment/Libraries

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
Obsoletes: mesa-dri-drivers-dri1 < 7.12
Obsoletes: mesa-dri-llvmcore <= 7.12
%description dri-drivers
Mesa-based DRI drivers.

%package vdpau-drivers
Summary: Mesa-based DRI drivers
Group: User Interface/X Hardware Support
Requires: mesa-dri-filesystem%{?_isa}
%description vdpau-drivers
Mesa-based VDPAU drivers.

%package -n khrplatform-devel
Summary: Khronos platform development package
Group: Development/Libraries
BuildArch: noarch

%description -n khrplatform-devel
Khronos platform development package

%package libGL-devel
Summary: Mesa libGL development package
Group: Development/Libraries
Requires: mesa-libGL = %{version}-%{release}
Requires: gl-manpages
Provides: libGL-devel

%description libGL-devel
Mesa libGL development package

%package libEGL-devel
Summary: Mesa libEGL development package
Group: Development/Libraries
Requires: mesa-libEGL = %{version}-%{release}
Requires: khrplatform-devel >= %{version}-%{release}

%description libEGL-devel
Mesa libEGL development package

%package libGLES-devel
Summary: Mesa libGLES development package
Group: Development/Libraries
Requires: mesa-libGLES = %{version}-%{release}
Requires: khrplatform-devel >= %{version}-%{release}

%description libGLES-devel
Mesa libGLES development package


%package libOSMesa
Summary: Mesa offscreen rendering libraries
Group: System Environment/Libraries
Provides: libOSMesa

%description libOSMesa
Mesa offscreen rendering libraries


%package libOSMesa-devel
Summary: Mesa offscreen rendering development package
Group: Development/Libraries
Requires: mesa-libOSMesa = %{version}-%{release}

%description libOSMesa-devel
Mesa offscreen rendering development package


%package libgbm
Summary: Mesa gbm library
Group: System Environment/Libraries
Provides: libgbm

%description libgbm
Mesa gbm runtime library.


%package libgbm-devel
Summary: Mesa libgbm development package
Group: Development/Libraries
Requires: mesa-libgbm%{?_isa} = %{version}-%{release}
Provides: libgbm-devel

%description libgbm-devel
Mesa libgbm development package


%if !0%{?rhel}
%package libwayland-egl
Summary: Mesa libwayland-egl library
Group: System Environment/Libraries
Provides: libwayland-egl

%description libwayland-egl
Mesa libwayland-egl runtime library.


%package libwayland-egl-devel
Summary: Mesa libwayland-egl development package
Group: Development/Libraries
Requires: mesa-libwayland-egl%{?_isa} = %{version}-%{release}
Provides: libwayland-egl-devel

%description libwayland-egl-devel
Mesa libwayland-egl development package
%endif


%if 0%{?with_vmware}
%package libxatracker
Summary: Mesa XA state tracker for vmware
Group: System Environment/Libraries
Provides: libxatracker

%description libxatracker
Mesa XA state tracker for vmware

%package libxatracker-devel
Summary: Mesa XA state tracker development package
Group: Development/Libraries
Requires: mesa-libxatracker%{?_isa} = %{version}-%{release}
Provides: libxatracker-devel

%description libxatracker-devel
Mesa XA state tracker development package
%endif

%package libglapi
Summary: Mesa shared glapi
Group: System Environment/Libraries

%description libglapi
Mesa shared glapi

%prep
#setup -q -n Mesa-%{version}%{?snapshot}
%setup -q -n mesa-%{gitdate}
grep -q ^/ src/gallium/auxiliary/vl/vl_decoder.c && exit 1
#patch0 -p1 -b .git
%patch1 -p1 -b .nv50rtti

# this fastpath is:
# - broken with swrast classic
# - broken on 24bpp
# - not a huge win anyway
# - ABI-broken wrt upstream
# - eventually obsoleted by vgem
#
# dear ajax: fix this one way or the other
#patch9 -p1 -b .shmget
#patch12 -p1 -b .16bpp

# hack from chromium - awaiting real upstream fix
%patch14 -p1 -b .snbfix

%patch15 -p1 -b .hwfloat
%patch16 -p1 -b .vdpau
%patch17 -p1 -b .tfp
%patch18 -p1 -b .be

%if 0%{with_private_llvm}
sed -i 's/llvm-config/mesa-private-llvm-config-%{__isa_bits}/g' configure.ac
sed -i 's/`$LLVM_CONFIG --version`/&-mesa/' configure.ac
%endif

# need to use libdrm_nouveau2 on F17
%if !0%{?rhel}
%if 0%{?fedora} < 18
sed -i 's/\<libdrm_nouveau\>/&2/' configure.ac
%endif
%endif

cp %{SOURCE4} docs/

%build

autoreconf --install  

export CFLAGS="$RPM_OPT_FLAGS"
# C++ note: we never say "catch" in the source.  we do say "typeid" once,
# in an assert, which is patched out above.  LLVM doesn't use RTTI or throw.
#
# We do say 'catch' in the clover and d3d1x state trackers, but we're not
# building those yet.
export CXXFLAGS="$RPM_OPT_FLAGS -fno-rtti -fno-exceptions"
%ifarch %{ix86}
# i do not have words for how much the assembly dispatch code infuriates me
%define common_flags --enable-selinux --enable-pic --disable-asm
%else
%define common_flags --enable-selinux --enable-pic
%endif

%configure %{common_flags} \
    --enable-osmesa \
    --with-dri-driverdir=%{_libdir}/dri \
    --enable-egl \
    --disable-gles1 \
    --enable-gles2 \
    --disable-gallium-egl \
    --disable-xvmc \
    --enable-vdpau \
    --with-egl-platforms=x11,drm%{?with_wayland:,wayland} \
    --enable-shared-glapi \
    --enable-gbm \
    --disable-opencl \
    --enable-glx-tls \
    --enable-texture-float=hardware \
    --enable-gallium-llvm \
    --with-llvm-shared-libs \
    --enable-dri \
%if %{with_hardware}
    %{?with_vmware:--enable-xa} \
    --with-gallium-drivers=%{?with_vmware:svga,}r300,r600,%{?with_radeonsi:radeonsi,}nouveau,swrast \
%else
    --with-gallium-drivers=swrast \
%endif
    %{?dri_drivers}

make %{?_smp_mflags} MKDEP=/bin/true

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%if 0%{?rhel}
# remove pre-DX9 drivers
rm -f $RPM_BUILD_ROOT%{_libdir}/dri/{radeon,r200,nouveau_vieux}_dri.*
%endif

# strip out useless headers
rm -f $RPM_BUILD_ROOT%{_includedir}/GL/w*.h

# remove .la files
find $RPM_BUILD_ROOT -name \*.la | xargs rm -f

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
%post libOSMesa -p /sbin/ldconfig
%postun libOSMesa -p /sbin/ldconfig
%post libEGL -p /sbin/ldconfig
%postun libEGL -p /sbin/ldconfig
%post libGLES -p /sbin/ldconfig
%postun libGLES -p /sbin/ldconfig
%post libglapi -p /sbin/ldconfig
%postun libglapi -p /sbin/ldconfig
%post libgbm -p /sbin/ldconfig
%postun libgbm -p /sbin/ldconfig
%if !0%{?rhel}
%post libwayland-egl -p /sbin/ldconfig
%postun libwayland-egl -p /sbin/ldconfig
%endif
%if 0%{?with_vmware}
%post libxatracker -p /sbin/ldconfig
%postun libxatracker -p /sbin/ldconfig
%endif

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
%{_libdir}/libGLESv2.so.2
%{_libdir}/libGLESv2.so.2.*

%files dri-filesystem
%defattr(-,root,root,-)
%doc docs/COPYING docs/Mesa-MLAA-License-Clarification-Email.txt
%dir %{_libdir}/dri
%dir %{_libdir}/vdpau

%files libglapi
%{_libdir}/libglapi.so.0
%{_libdir}/libglapi.so.0.*

%files dri-drivers
%defattr(-,root,root,-)
%if %{with_hardware}
%config(noreplace) %{_sysconfdir}/drirc
%if !0%{?rhel}
%{_libdir}/dri/radeon_dri.so
%{_libdir}/dri/r200_dri.so
%{_libdir}/dri/nouveau_vieux_dri.so
%endif
%{_libdir}/dri/r300_dri.so
%{_libdir}/dri/r600_dri.so
%if 0%{?with_radeonsi}
%{_libdir}/dri/radeonsi_dri.so
%endif
%ifarch %{ix86} x86_64
%{_libdir}/dri/i915_dri.so
%{_libdir}/dri/i965_dri.so
%endif
%{_libdir}/dri/nouveau_dri.so
%if 0%{?with_vmware}
%{_libdir}/dri/vmwgfx_dri.so
%endif
%else
%exclude %{_sysconfdir}/drirc
%endif
%{_libdir}/libdricore*.so*
%{_libdir}/dri/swrast_dri.so

%if %{with_hardware}
# should be explicit here but meh
%files vdpau-drivers
%defattr(-,root,root,-)
%{_libdir}/vdpau/*.so*
%endif

%files -n khrplatform-devel
%defattr(-,root,root,-)
%{_includedir}/KHR

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
%{_libdir}/libglapi.so
%{_libdir}/pkgconfig/gl.pc

%files libEGL-devel
%defattr(-,root,root,-)
%dir %{_includedir}/EGL
%{_includedir}/EGL/eglext.h
%{_includedir}/EGL/egl.h
%{_includedir}/EGL/eglmesaext.h
%{_includedir}/EGL/eglplatform.h
%dir %{_includedir}/KHR
%{_includedir}/KHR/khrplatform.h
%{_libdir}/pkgconfig/egl.pc
%{_libdir}/libEGL.so

%files libGLES-devel
%defattr(-,root,root,-)
%dir %{_includedir}/GLES2
%{_includedir}/GLES2/gl2platform.h
%{_includedir}/GLES2/gl2.h
%{_includedir}/GLES2/gl2ext.h
%{_includedir}/GLES3/gl3platform.h
%{_includedir}/GLES3/gl3.h
%{_includedir}/GLES3/gl3ext.h
%{_libdir}/pkgconfig/glesv2.pc
%{_libdir}/libGLESv2.so

%files libOSMesa
%defattr(-,root,root,-)
%doc docs/COPYING
%{_libdir}/libOSMesa.so.8*

%files libOSMesa-devel
%defattr(-,root,root,-)
%dir %{_includedir}/GL
%{_includedir}/GL/osmesa.h
%{_libdir}/libOSMesa.so
%{_libdir}/pkgconfig/osmesa.pc

%files libgbm
%defattr(-,root,root,-)
%doc docs/COPYING
%{_libdir}/libgbm.so.1
%{_libdir}/libgbm.so.1.*

%files libgbm-devel
%defattr(-,root,root,-)
%{_libdir}/libgbm.so
%{_includedir}/gbm.h
%{_libdir}/pkgconfig/gbm.pc

%if !0%{?rhel}
%files libwayland-egl
%defattr(-,root,root,-)
%doc docs/COPYING
%{_libdir}/libwayland-egl.so.1
%{_libdir}/libwayland-egl.so.1.*

%files libwayland-egl-devel
%defattr(-,root,root,-)
%{_libdir}/libwayland-egl.so
%{_libdir}/pkgconfig/wayland-egl.pc
%endif

%if 0%{?with_vmware}
%files libxatracker
%defattr(-,root,root,-)
%doc docs/COPYING
%if %{with_hardware}
%{_libdir}/libxatracker.so.1
%{_libdir}/libxatracker.so.1.*
%endif

%files libxatracker-devel
%defattr(-,root,root,-)
%if %{with_hardware}
%{_libdir}/libxatracker.so
%{_includedir}/xa_tracker.h
%{_includedir}/xa_composite.h
%{_includedir}/xa_context.h
%{_libdir}/pkgconfig/xatracker.pc
%endif
%endif

%changelog
* Wed May 08 2013 Adam Jackson <ajax@redhat.com> 9.2-0.1.20130508
- Switch to Mesa master (pre 9.2)
- Fix llvmpipe on big-endian and enable llvmpipe everywhere
- Build vdpau drivers for r600/radeonsi/nouveau
- Enable hardware floating-point texture support
- Drop GLESv1, nothing's using it, let's not start

* Sat Apr 27 2013 Dave Airlie <airlied@redhat.com> 9.1.1-1
- rebase to Mesa 9.1.1 + fixes from git

* Thu Apr 11 2013 Dave Airlie <airlied@redhat.com> 9.1-6
- enable glx tls for glamor to work properly

* Thu Apr 04 2013 Adam Jackson <ajax@redhat.com> 9.1-5
- Enable llvmpipe even on non-SSE2 machines (#909473)

* Tue Mar 26 2013 Adam Jackson <ajax@redhat.com> 9.1-4
- Fix build with private LLVM

* Tue Mar 19 2013 Adam Jackson <ajax@redhat.com> 9.1-3
- mesa-9.1-53-gd0ccb5b.patch: Sync with today's git

* Tue Mar 19 2013 Dave Airlie <airlied@redhat.com> 9.1-2
- add SNB hang workaround from chromium

* Fri Mar 08 2013 Adam Jackson <ajax@redhat.com> 9.1-1
- Mesa 9.1

* Wed Feb 27 2013 Dan Horák <dan[at]danny.cz> - 9.1-0.4
- /etc/drirc is always created, so exclude it on platforms without hw drivers

* Tue Feb 26 2013 Adam Jackson <ajax@redhat.com> 9.1-0.3
- Fix s390*'s swrast to be classic not softpipe

* Tue Feb 19 2013 Jens Petersen <petersen@redhat.com> - 9.1-0.2
- build against llvm-3.2
- turn on radeonsi

* Wed Feb 13 2013 Dave Airlie <airlied@redhat.com> 9.1-0.1
- snapshot mesa 9.1 branch

* Tue Jan 15 2013 Tom Callaway <spot@fedoraproject.org> 9.0.1-4
- clarify license on pp_mlaa* files

* Thu Dec 20 2012 Adam Jackson <ajax@redhat.com> 9.0.1-3
- mesa-9.0.1-22-gd0a9ab2.patch: Sync with git
- Build with -fno-rtti -fno-exceptions, modest size and speed win
- mesa-9.0.1-less-cxx-please.patch: Remove the only use of typeid() so the
  above works.

* Wed Dec 05 2012 Adam Jackson <ajax@redhat.com> 9.0.1-2
- Allow linking against a private version of LLVM libs for RHEL7
- Build with -j again

* Mon Dec 03 2012 Adam Jackson <ajax@redhat.com> 9.0.1-1
- Mesa 9.0.1

* Wed Nov 07 2012 Dave Airlie <airlied@redhat.com> 9.0-5
- mesa-9.0-19-g895a587.patch: sync with 9.0 branch with git
- drop wayland patch its in git now.

* Thu Nov 01 2012 Adam Jackson <ajax@redhat.com> 9.0-4
- mesa-9.0-18-g5fe5aa8: sync with 9.0 branch in git
- Portability fixes for F17: old wayland, old llvm.

* Sat Oct 27 2012 Dan Horák <dan[at]danny.cz> 9.0-3
- gallium drivers must be set explicitely for s390(x) otherwise also r300, r600 and vmwgfx are built

* Fri Oct 19 2012 Adam Jackson <ajax@redhat.com> 9.0-2
- Rebuild for wayland 0.99

* Wed Oct 10 2012 Adam Jackson <ajax@redhat.com> 9.0-1
- Mesa 9.0
- mesa-9.0-12-gd56ee24.patch: sync with 9.0 branch in git

* Wed Oct 10 2012 Adam Jackson <ajax@redhat.com> 9.0-0.4
- Switch to external gl-manpages and libGLU
- Drop ShmGetImage fastpath for a bit

* Mon Oct 01 2012 Dan Horák <dan[at]danny.cz> 9.0-0.3
- explicit BR: libGL-devel is required on s390(x), it's probbaly brought in indirectly on x86
- gallium drivers must be set explicitely for s390(x) otherwise also r300, r600 and vmwgfx are built

* Mon Sep 24 2012 Adam Jackson <ajax@redhat.com> 9.0-0.2
- Switch to swrast classic instead of softpipe for non-llvm arches
- Re-disable llvm on ppc until it can draw pixels

* Mon Sep 24 2012 Dave Airlie <airlied@redhat.com> 9.0-0.1
- rebase to latest upstream 9.0 pre-release branch
- add back glu from new upstream (split for f18 later)

* Fri Sep 14 2012 Dave Airlie <airlied@redhat.com> 8.1-0.21
- why fix one yylex when you can fix two

* Fri Sep 14 2012 Dave Airlie <airlied@redhat.com> 8.1-0.20
- fix yylex collision reported on irc by hughsie

* Mon Aug 27 2012 Adam Jackson <ajax@redhat.com> 8.1-0.19
- Today's git snap
- Revert dependency on libkms
- Patch from Mageia to fix some undefined symbols

* Fri Aug 17 2012 Dave Airlie <airlied@redhat.com> 8.1-0.18
- parallel make seems broken - on 16 way machine internally.

* Thu Aug 16 2012 Dave Airlie <airlied@redhat.com> 8.1-0.17
- upstream snapshot

* Wed Jul 25 2012 Peter Robinson <pbrobinson@fedoraproject.org> 8.1-0.16
- Enable LLVM on ARM

* Wed Jul 25 2012 Peter Robinson <pbrobinson@fedoraproject.org> 8.1-0.15
- Fix building on platforms with HW and without LLVM

* Tue Jul 24 2012 Adam Jackson <ajax@redhat.com> 8.1-0.14
- Re-enable llvm on ppc, being worked on
- Don't BuildReq on wayland things in RHEL

* Mon Jul 23 2012 Adam Jackson <ajax@redhat.com> 8.1-0.13
- Build radeonsi (#842194)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.1-0.12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Dave Airlie <airlied@redhat.com> 8.1-0.11
- upstream snapshot: fixes build issues

* Tue Jul 17 2012 Dave Airlie <airlied@redhat.com> 8.1-0.10
- snapshot mesa: add some build hackarounds 

* Sat Jul 14 2012 Ville Skyttä <ville.skytta@iki.fi> - 8.1-0.9
- Call ldconfig at -libglapi and -libxatracker post(un)install time.
- Drop redundant ldconfig dependencies, let rpm auto-add them.

* Wed Jun 13 2012 Dave Airlie <airlied@redhat.com> 8.1-0.8
- enable shared llvm usage.

* Thu Jun 07 2012 Adam Jackson <ajax@redhat.com> 8.1-0.7
- Disable llvm on non-x86 (#829020)

* Sun Jun 03 2012 Dave Airlie <airlied@redhat.com> 8.1-0.6
- rebase to git master + build on top of llvm 3.1

* Thu May 17 2012 Adam Jackson <ajax@redhat.com> 8.1-0.5
- mesa-8.0-llvmpipe-shmget.patch: Rediff for 8.1.

* Thu May 10 2012 Karsten Hopp <karsten@redhat.com> 8.1-0.4
- revert disabling of hardware drivers, disable only llvm on PPC*
  (#819060)

* Tue May 01 2012 Adam Jackson <ajax@redhat.com> 8.1-0.3
- More RHEL tweaking: no pre-DX7 drivers, no wayland.

* Thu Apr 26 2012 Karsten Hopp <karsten@redhat.com> 8.1-0.2
- move drirc into with_hardware section (Dave Airlie)
- libdricore.so and libglsl.so get built and installed on
  non-hardware archs, include them in the file list

* Thu Apr 26 2012 Adam Jackson <ajax@redhat.com> 8.1-0.2
- Don't build vmware stuff on non-x86 (#815444)

* Tue Apr 24 2012 Richard Hughes <rhughes@redhat.com> 8.0.3-0.1
- Rebuild with new git snapshot
- Remove upstreamed patches

* Tue Apr 24 2012 Karsten Hopp <karsten@redhat.com> 8.0.2-4
- disable llvm on PPC(64) in Fedora as recommended in bugzilla 769803

* Tue Apr 10 2012 Adam Jackson <ajax@redhat.com> 8.0.2-3
- Require newer libX11 on F17+

* Mon Apr 02 2012 Adam Jackson <ajax@redhat.com> 8.0.2-2
- mesa-8.0.1-fix-16bpp.patch: Fix 16bpp in llvmpipe

* Sat Mar 31 2012 Dave Airlie <airlied@redhat.com> 8.0.2-1
- get latest 8.0.2 set of fixes

* Wed Mar 28 2012 Adam Jackson <ajax@redhat.com> 8.0.1-9
- Subpackage libglapi instead of abusing -dri-drivers for it to keep minimal
  disk space minimal. (#807750)

* Wed Mar 28 2012 Adam Jackson <ajax@redhat.com> 8.0.1-8
- mesa-8.0.1-llvmpipe-shmget.patch: Fix image pitch bug.

* Fri Mar 23 2012 Adam Jackson <ajax@redhat.com> 8.0.1-7
- mesa-8.0-nouveau-tfp-blacklist.patch: gnome-shell blacklisting: nvfx and
  below with <= 64M of vram, and all nv30.

* Wed Mar 21 2012 Adam Jackson <ajax@redhat.com> 8.0.1-6
- mesa-8.0.1-llvmpipe-shmget.patch: Use ShmGetImage if possible

* Mon Mar 19 2012 Adam Jackson <ajax@redhat.com> 8.0.1-5
- Move libglapi into -dri-drivers instead of -libGLES as being marginally
  more appropriate (libGL wants to have DRI drivers, but doesn't need to
  have a full libGLES too).

* Thu Mar 15 2012 Dave Airlie <airlied@gmail.com> 8.0.1-4
- enable vmwgfx + xa state tracker

* Thu Mar 01 2012 Adam Jackson <ajax@redhat.com> 8.0.1-3
- mesa-8.0.1-git.patch: Sync with 8.0 branch (commit a3080987)

* Sat Feb 18 2012 Thorsten Leemhuis <fedora@leemhuis.info> 8.0.1-2
- a few changes for weston, the wayland reference compositor (#790542):
- enable gbm and shared-glapi in configure command (the latter is required by 
  the former) and add subpackages libgbm and libgbm-devel
- add --with-egl-platforms=x11,wayland,drm to configure command and add 
  subpackages libwayland-egl and libwayland-egl-devel

* Fri Feb 17 2012 Adam Jackson <ajax@redhat.com> 8.0.1-1
- Mesa 8.0.1

* Mon Feb 13 2012 Adam Jackson <ajax@redhat.com> 8.0-1
- Mesa 8.0

* Mon Feb 13 2012 Adam Jackson <ajax@redhat.com> 8.0-0.2
- Default to DRI libGL on all arches (#789402)

* Thu Jan 26 2012 Dave Airlie <airlied@redhat.com> 8.0-0.1
- initial 8.0 snapshot

* Thu Jan 05 2012 Adam Jackson <ajax@redhat.com> 7.12-0.7
- Today's git snapshot

* Wed Dec 14 2011 Adam Jackson <ajax@redhat.com> 7.12-0.6
- Today's git snapshot
- Disable hardware drivers on ppc* in RHEL

* Fri Dec 02 2011 Dan Horák <dan[at]danny.cz> 7.12-0.5
- fix build on s390(x)

* Tue Nov 29 2011 Adam Jackson <ajax@redhat.com> 7.12-0.4
- Today's git snapshot
- --enable-xcb
- mesa-7.1-nukeglthread-debug.patch: Drop

* Thu Nov 17 2011 Adam Jackson <ajax@redhat.com> 7.12-0.3
- mesa-dri-drivers Obsoletes: mesa-dri-drivers-dri1 < 7.12

* Wed Nov 16 2011 Adam Jackson <ajax@redhat.com> 7.12-0.2
- Cleanups to BuildRequires, Requires, Conflicts, etc.

* Mon Nov 14 2011 Dave Airlie <airlied@redhat.com> 7.12-0.1
- rebase to upstream snapshot of 7.12

* Mon Nov 14 2011 Adam Jackson <ajax@redhat.com> 7.11-12
- Rebuild for new libllvm soname

* Wed Nov 09 2011 Adam Jackson <ajax@redhat.com> 7.11-11
- Obsolete more -llvmcore (#752152)

* Thu Nov 03 2011 Dave Airlie <airlied@redhat.com> 7.11-10
- snapshot latest mesa 7.11 stable branch (what will be 7.11.1)

* Thu Nov 03 2011 Adam Jackson <ajax@redhat.com> 7.11-9
- mesa-7.11-fix-sw-24bpp.patch: Fix software rendering in 24bpp.

* Fri Oct 28 2011 Adam Jackson <ajax@redhat.com> 7.11-8
- mesa-7.11-intel-swap-event.patch: Disable GLX_INTEL_swap_event by default;
  DRI2 enables it explicitly, but swrast doesn't and oughtn't. (#748747)

* Mon Oct 24 2011 Adam Jackson <ajax@redhat.com> 7.11-6
- 0001-nv50-fix-max-texture-levels.patch: Fix maximum texture size on
  nouveau (and thus, gnome-shell init on wide display setups) (#748540)

* Mon Oct 24 2011 Adam Jackson <ajax@redhat.com> 7.11-5
- mesa-7.11-drisw-glx13.patch: Fix GLX 1.3 ctors with swrast (#747276)

* Fri Sep 09 2011 Adam Jackson <ajax@redhat.com> 7.11-4
- mesa-7.11-generic-wmb.patch: Add generic write memory barrier macro for
  non-PC arches.

* Thu Sep 08 2011 Adam Jackson <ajax@redhat.com> 7.11-3
- Add khrplatform-devel subpackage so {EGL,GLES}-devel are usable

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
