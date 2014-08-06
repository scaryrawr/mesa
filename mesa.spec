%if 0%{?rhel}
%define with_private_llvm 1
%define with_wayland 0
%else
%define with_private_llvm 0
%define with_vdpau 1
%define with_wayland 1
%endif

%ifarch ppc64le
%undefine with_vdpau
%endif

# S390 doesn't have video cards, but we need swrast for xserver's GLX
# llvm (and thus llvmpipe) doesn't actually work on ppc32
%ifnarch s390 ppc  ppc64le
%define with_llvm 1
%endif

%define min_wayland_version 1.0
%if 0%{?with_llvm}
%define with_radeonsi 1
%endif

%ifarch s390 s390x ppc64le ppc
%define with_hardware 0
%define base_drivers swrast
%endif
%ifnarch s390 s390x ppc64le ppc
%define with_hardware 1
%define base_drivers nouveau,radeon,r200
%ifarch %{ix86} x86_64
%define platform_drivers ,i915,i965
%define with_vmware 1
%define with_xa     1
%define with_opencl 1
%define with_omx    1
%endif
%ifarch %{arm} aarch64
%define with_freedreno 1
%define with_xa        1
%define with_omx       1
%endif
%endif

%define dri_drivers --with-dri-drivers=%{?base_drivers}%{?platform_drivers}

%define _default_patch_fuzz 2

#% define gitdate 20140510
%define githash c40d7d6d948912a4d51cbf8f0854cf2ebe916636
%define git %{?githash:%{githash}}%{!?githash:%{gitdate}}

Summary: Mesa graphics libraries
Name: mesa
Version: 10.3
Release: 0.devel.2.%{git}%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.mesa3d.org

# Source0: MesaLib-%{version}.tar.xz
Source0: %{name}-%{git}.tar.xz
Source1: sanitize-tarball.sh
Source2: make-release-tarball.sh
Source3: make-git-snapshot.sh

# src/gallium/auxiliary/postprocess/pp_mlaa* have an ... interestingly worded license.
# Source4 contains email correspondence clarifying the license terms.
# Fedora opts to ignore the optional part of clause 2 and treat that code as 2 clause BSD.
Source4: Mesa-MLAA-License-Clarification-Email.txt

Patch1: mesa-10.0-nv50-fix-build.patch
Patch9: mesa-8.0-llvmpipe-shmget.patch
Patch12: mesa-8.0.1-fix-16bpp.patch
Patch15: mesa-9.2-hardware-float.patch
Patch20: mesa-10.2-evergreen-big-endian.patch

# https://bugs.freedesktop.org/show_bug.cgi?id=73512
Patch99: 0001-opencl-use-versioned-.so-in-mesa.icd.patch

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
BuildRequires: libxshmfence-devel
BuildRequires: elfutils
BuildRequires: python
BuildRequires: gettext
%if 0%{?with_llvm}
%if 0%{?with_private_llvm}
BuildRequires: mesa-private-llvm-devel
%else
BuildRequires: llvm-devel >= 3.4-7
%if 0%{?with_opencl}
BuildRequires: clang-devel >= 3.0
%endif
%endif
%endif
BuildRequires: elfutils-libelf-devel
BuildRequires: libxml2-python
BuildRequires: libudev-devel
BuildRequires: bison flex
%if 0%{?with_wayland}
BuildRequires: pkgconfig(wayland-client) >= %{min_wayland_version}
BuildRequires: pkgconfig(wayland-server) >= %{min_wayland_version}
%endif
BuildRequires: mesa-libGL-devel
%if 0%{?with_vdpau}
BuildRequires: libvdpau-devel
%endif
BuildRequires: zlib-devel
%if 0%{?with_omx}
BuildRequires: libomxil-bellagio-devel
%endif
%if 0%{?with_opencl}
BuildRequires: libclc-devel llvm-static opencl-filesystem
%endif

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

%package filesystem
Summary: Mesa driver filesystem
Group: User Interface/X Hardware Support
Provides: mesa-dri-filesystem = %{version}-%{release}
Obsoletes: mesa-dri-filesystem < %{version}-%{release}
%description filesystem
Mesa driver filesystem

%package dri-drivers
Summary: Mesa-based DRI drivers
Group: User Interface/X Hardware Support
Requires: mesa-filesystem%{?_isa}
Obsoletes: mesa-dri-drivers-dri1 < 7.12
Obsoletes: mesa-dri-llvmcore <= 7.12
%description dri-drivers
Mesa-based DRI drivers.

%if 0%{?with_omx}
%package omx-drivers
Summary: Mesa-based OMX drivers
Group: User Interface/X Hardware Support
Requires: mesa-filesystem%{?_isa}
Requires: libomxil-bellagio%{?_isa}
%description omx-drivers
Mesa-based OMX drivers.
%endif

%if 0%{?with_vdpau}
%package vdpau-drivers
Summary: Mesa-based DRI drivers
Group: User Interface/X Hardware Support
Requires: mesa-filesystem%{?_isa}
%description vdpau-drivers
Mesa-based VDPAU drivers.
%endif

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
Provides: khrplatform-devel = %{version}-%{release}
Obsoletes: khrplatform-devel < %{version}-%{release}

%description libEGL-devel
Mesa libEGL development package

%package libGLES-devel
Summary: Mesa libGLES development package
Group: Development/Libraries
Requires: mesa-libGLES = %{version}-%{release}

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


%if 0%{?with_wayland}
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


%if 0%{?with_xa}
%package libxatracker
Summary: Mesa XA state tracker
Group: System Environment/Libraries
Provides: libxatracker

%description libxatracker
Mesa XA state tracker

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


%if 0%{?with_opencl}
%package libOpenCL
Summary: Mesa OpenCL runtime library
Requires: ocl-icd
Requires: libclc
Requires: mesa-libgbm = %{version}-%{release}

%description libOpenCL
Mesa OpenCL runtime library.

%package libOpenCL-devel
Summary: Mesa OpenCL development package
Requires: mesa-libOpenCL%{?_isa} = %{version}-%{release}

%description libOpenCL-devel
Mesa OpenCL development package.
%endif

%prep
#setup -q -n Mesa-%{version}%{?snapshot}
%setup -q -n mesa-%{git}
grep -q ^/ src/gallium/auxiliary/vl/vl_decoder.c && exit 1
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

%patch15 -p1 -b .hwfloat
%patch20 -p1 -b .egbe

%if 0%{?with_opencl}
%patch99 -p1 -b .icd
%endif

%if 0%{with_private_llvm}
sed -i 's/llvm-config/mesa-private-llvm-config-%{__isa_bits}/g' configure.ac
sed -i 's/`$LLVM_CONFIG --version`/&-mesa/' configure.ac
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
export CXXFLAGS="$RPM_OPT_FLAGS %{?with_opencl:-frtti -fexceptions} %{!?with_opencl:-fno-rtti -fno-exceptions}"
%ifarch %{ix86}
# i do not have words for how much the assembly dispatch code infuriates me
%define asm_flags --disable-asm
%endif

%configure \
    %{?asm_flags} \
    --enable-selinux \
    --enable-osmesa \
    --with-dri-driverdir=%{_libdir}/dri \
    --enable-egl \
    --disable-gles1 \
    --enable-gles2 \
%if %{with_hardware}
    --enable-gallium-egl \
%endif
    --disable-xvmc \
    %{?with_vdpau:--enable-vdpau} \
    --with-egl-platforms=x11,drm%{?with_wayland:,wayland} \
    --enable-shared-glapi \
    --enable-gbm \
    %{?with_omx:--enable-omx} \
    %{?with_opencl:--enable-opencl --enable-opencl-icd --with-clang-libdir=%{_prefix}/lib} %{!?with_opencl:--disable-opencl} \
    --enable-glx-tls \
    --enable-texture-float=yes \
    %{?with_llvm:--enable-gallium-llvm} \
    %{?with_llvm:--enable-llvm-shared-libs} \
    --enable-dri \
%if %{with_hardware}
    %{?with_xa:--enable-xa} \
    --with-gallium-drivers=%{?with_vmware:svga,}%{?with_radeonsi:radeonsi,}%{?with_llvm:swrast,r600,}%{?with_freedreno:freedreno,}r300,nouveau \
%else
    --with-gallium-drivers=%{?with_llvm:swrast} \
%endif
%if 0%{?fedora} < 21
    --disable-dri3 \
%endif
    %{?dri_drivers}

# this seems to be neccessary for s390
make -C src/mesa/drivers/dri/common/xmlpool/

make %{?_smp_mflags} MKDEP=/bin/true

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%if 0%{?rhel}
# remove pre-DX9 drivers
rm -f $RPM_BUILD_ROOT%{_libdir}/dri/{radeon,r200,nouveau_vieux}_dri.*
%endif

%if !%{with_hardware}
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/drirc
%endif

# libvdpau opens the versioned name, don't bother including the unversioned
rm -f $RPM_BUILD_ROOT%{_libdir}/vdpau/*.so

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
%if 0%{?with_wayland}
%post libwayland-egl -p /sbin/ldconfig
%postun libwayland-egl -p /sbin/ldconfig
%endif
%if 0%{?with_xa}
%post libxatracker -p /sbin/ldconfig
%postun libxatracker -p /sbin/ldconfig
%endif
%if 0%{?with_opencl}
%post libOpenCL -p /sbin/ldconfig
%postun libOpenCL -p /sbin/ldconfig
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
%if %{with_hardware}
%dir %{_libdir}/egl
%{_libdir}/egl/egl_gallium.so
%endif

%files libGLES
%defattr(-,root,root,-)
%doc docs/COPYING
%{_libdir}/libGLESv2.so.2
%{_libdir}/libGLESv2.so.2.*

%files filesystem
%defattr(-,root,root,-)
%doc docs/COPYING docs/Mesa-MLAA-License-Clarification-Email.txt
%dir %{_libdir}/dri
%if %{with_hardware}
%if 0%{?with_vdpau}
%dir %{_libdir}/vdpau
%endif
%endif

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
%if 0%{?with_llvm}
%{_libdir}/dri/r600_dri.so
%if 0%{?with_radeonsi}
%{_libdir}/dri/radeonsi_dri.so
%endif
%endif
%ifarch %{ix86} x86_64
%{_libdir}/dri/i915_dri.so
%{_libdir}/dri/i965_dri.so
%endif
%if 0%{?with_freedreno}
%{_libdir}/dri/freedreno_dri.so
%endif
%{_libdir}/dri/nouveau_dri.so
%if 0%{?with_vmware}
%{_libdir}/dri/vmwgfx_dri.so
%endif
%dir %{_libdir}/gallium-pipe
%{_libdir}/gallium-pipe/*.so
%endif
%{_libdir}/dri/swrast_dri.so
%{_libdir}/dri/kms_swrast_dri.so

%if %{with_hardware}
%if 0%{?with_omx}
%files omx-drivers
%defattr(-,root,root,-)
%{_libdir}/bellagio/libomx_mesa.so
%endif
%if 0%{?with_vdpau}
%files vdpau-drivers
%defattr(-,root,root,-)
%{_libdir}/vdpau/libvdpau_nouveau.so.1*
%if 0%{?with_llvm}
%{_libdir}/vdpau/libvdpau_r600.so.1*
%if 0%{?with_radeonsi}
%{_libdir}/vdpau/libvdpau_radeonsi.so.1*
%endif
%endif
%endif
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
%{_libdir}/libglapi.so
%{_libdir}/pkgconfig/gl.pc

%files libEGL-devel
%defattr(-,root,root,-)
%dir %{_includedir}/EGL
%{_includedir}/EGL/eglext.h
%{_includedir}/EGL/egl.h
%{_includedir}/EGL/eglmesaext.h
%{_includedir}/EGL/eglplatform.h
%{_includedir}/EGL/eglextchromium.h
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
%{_includedir}/GLES3/gl31.h
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
%if %{with_hardware}
%dir %{_libdir}/gbm
%{_libdir}/gbm/gbm_gallium_drm.so
%endif

%files libgbm-devel
%defattr(-,root,root,-)
%{_libdir}/libgbm.so
%{_includedir}/gbm.h
%{_libdir}/pkgconfig/gbm.pc

%if 0%{?with_wayland}
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

%if 0%{?with_xa}
%files libxatracker
%defattr(-,root,root,-)
%doc docs/COPYING
%if %{with_hardware}
%{_libdir}/libxatracker.so.2
%{_libdir}/libxatracker.so.2.*
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

%if 0%{?with_opencl}
%files libOpenCL
%{_libdir}/libMesaOpenCL.so.*
%{_sysconfdir}/OpenCL/vendors/mesa.icd

%files libOpenCL-devel
%{_libdir}/libMesaOpenCL.so
%endif

# Generate changelog using:
# git log old_commit_sha..new_commit_sha --format="- %H: %s (%an)"
%changelog
* Wed Aug 06 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.3-0.devel.2.c40d7d6d948912a4d51cbf8f0854cf2ebe916636
- dri/xmlconfig: s/uint/unsigned int/ (Vinson Lee)
- mesa include stdint.h in formats.h (Brian Paul)
- mesa/texstore: Add a generic rgba integer texture upload path (Jason Ekstrand)
- mesa/texstore: Add a generic float/normalized rgba texture upload path (Jason Ekstrand)
- mesa/texstore: Use _mesa_swizzle_and_convert when possible (Jason Ekstrand)
- main/texstore: Split texture storage into three functions (Jason Ekstrand)
- mesa/format_utils: Add a function to convert a mesa_format to an array format (Jason Ekstrand)
- mesa/format_utils: Add a general format conversion function (Jason Ekstrand)
- mesa/imports: Add a _mesa_half_is_negative helper function (Jason Ekstrand)
- mesa/formats: Add layout and swizzle information (Jason Ekstrand)
- mesa/formats: Remove IndexBits (Jason Ekstrand)
- mesa/formats: Autogenerate the format_info structure from a CSV file (Jason Ekstrand)
- mesa/main: Add python code to generate the format_info structure (Jason Ekstrand)
- mesa: Add python to parse the formats CSV file (Jason Ekstrand)
- mesa: Add a format description CSV file (Jason Ekstrand)
- util/tests/hash_table: Link against libmesautil instead of libmesa (Jason Ekstrand)
- st/mesa: adjust Z coordinates for quad clearing (Brian Paul)
- mesa: make vertex array type error checking a little more efficient (Brian Paul)
- glsl_to_tgsi: Fix typo shader_program -> shader (Michel Dänzer)
- mesa: update wglext.h to version 20140630 (Brian Paul)
- mesa: update glxext.h to version 20140725 (Brian Paul)
- mesa: update glext.h to version 20140725 (Brian Paul)
- meta: Disable dithering during glBlitFramebuffer (Neil Roberts)
- libgl-xlib: drop duplicate mesautil from scons build (Emil Velikov)
- llvmpipe/tests: automake: link against libmesautil.la (Emil Velikov)
- gallium/tests: automake: link against libmesautil.la (Emil Velikov)
- targets/omx: automake: link against libmesautil.la (Emil Velikov)
- targets/xvmc: automake: link against libmesautil.la (Emil Velikov)
- targets/clover: link against libmesautil.la (Jan Vesely)
- gallivm: Fix build with latest LLVM (Jan Vesely)
- targets/dri: link with mesautil (Roland Scheidegger)
- gallium/docs: Document TEX2/TXL2/TXB2 instructions and fix up other tex doc (Roland Scheidegger)
- gallivm: fix cube map array (and cube map shadow with bias) handling (Roland Scheidegger)
- llvmpipe: implement support for cube map arrays (Roland Scheidegger)
- egl: Fix OpenGL ES version checks in _eglParseContextAttribList() (Anuj Phogat)
- meta: Fix datatype computation in get_temp_image_type() (Anuj Phogat)
- meta: Move the call to _mesa_get_format_datatype() out of switch (Anuj Phogat)
- meta: Use _mesa_get_format_bits() to get the GL_RED_BITS (Anuj Phogat)
- meta: Initialize the variable in declaration statement (Anuj Phogat)
- mesa: Allow GL_TEXTURE_CUBE_MAP target with compressed internal formats (Anuj Phogat)
- mesa: Add gles3 condition for normalized internal formats in glCopyTexImage*() (Anuj Phogat)
- mesa: Add utility function _mesa_is_enum_format_unorm() (Anuj Phogat)
- mesa: Add gles3 error condition for GL_RGBA10_A2 buffer format in glCopyTexImage*() (Anuj Phogat)
- mesa: Add a gles3 error condition for sized internalformat in glCopyTexImage*() (Anuj Phogat)
- mesa: Add a helper function _mesa_is_enum_format_unsized() (Anuj Phogat)
- mesa: Don't allow snorm internal formats in glCopyTexImage*() in GLES3 (Anuj Phogat)
- mesa: Add utility function _mesa_is_enum_format_snorm() (Anuj Phogat)
- mesa: Fix condition for using compressed internalformat in glCompressedTexImage3D() (Anuj Phogat)
- mesa: Add error condition for using compressed internalformat in glTexStorage3D() (Anuj Phogat)
- mesa: Turn target_can_be_compressed() in to a utility function (Anuj Phogat)
- mesa: Fix error condition for valid texture targets in glTexStorage* functions (Anuj Phogat)
- glsl: Rebuild the symbol table without unreachable symbols (Ian Romanick)
- glsl: Only create one ir_function for a given name. (Kenneth Graunke)
- glsl: Make it possible to ignore built-ins when matching signatures. (Kenneth Graunke)
- mesa: Actually use the Mesa IR optimizer for ARB programs. (Kenneth Graunke)
- glsl: Do not add extra padding to structures (Ian Romanick)
- glsl: Correctly determine when the field of a UBO is row-major (Ian Romanick)
- linker: Use the matrix layout information in ir_variable and glsl_type for UBO layout (Ian Romanick)
- glsl: Track matrix layout of variables using two bits (Ian Romanick)
- glsl: Also track matrix layout information into structures (Ian Romanick)
- glsl: Track matrix layout of structure fields using two bits (Ian Romanick)
- glsl: Correctly load columns of a row-major matrix (Ian Romanick)
- linker: Add padding after the last field of a structure (Ian Romanick)
- linker: Add a last_field parameter to various program_resource_visitor methods (Ian Romanick)
- mesa: Do not list inactive block members as active (Ian Romanick)
- glsl: Do not eliminate 'shared' or 'std140' blocks or block members (Ian Romanick)
- glsl: Use the without_array predicate to simplify some code (Ian Romanick)
- glsl: Add without_array type predicate (Ian Romanick)
- glsl: Use constant_expression_value instead of as_constant (Ian Romanick)
- targets/graw-gdi: link with mesautil, not mesautils (Brian Paul)
- wmesa: link with mesautil (Brian Paul)
- osmesa: link with mesautil (Brian Paul)
- targets/libgl-gdi: link with mesautil (Brian Paul)
- targets/egl-static: link with libmesautil.la (Brian Paul)
- mesa/x86: put code in braces to silence declarations after code warning (Brian Paul)
- src/Makefile.am: Move gtest before util (Jason Ekstrand)
- util: include c99_compat.h in format_srgb.h to get 'inline' definition (Brian Paul)
- util: include c99_compat.h in hash_table.h to get 'inline' definition (Brian Paul)
- targets/vdpau: link with libmesautil.la to fix build breakage (Brian Paul)
- xlib: fix missing mesautil build breakage (Brian Paul)
- svga: SVGA_3D_CMD_BIND_GB_SHADER needs to reserve two relocations. (Matthew McClure)
- gallium: Add libmesautil dependency to gdm and xa targets (Jason Ekstrand)
- mesa/main: Use the RGB <-> sRGB conversion functions in libmesautil (Jason Ekstrand)
- gallium: Move sRGB <-> RGB handling to libmesautil (Jason Ekstrand)
- util: Gather some common macros (Jason Ekstrand)
- util: Move the open-addressing linear-probing hash_table to src/util. (Kenneth Graunke)
- util: Move ralloc to a new src/util directory. (Kenneth Graunke)
- mesa/SConscript: Use Makefile.sources instead of duplicating the file lists (Jason Ekstrand)
- targets/dri: resolve the scons build (Emil Velikov)
- mesa/st: Fix compiler warnings (Jan Vesely)
- gallium: Fix compiler warning. (Jan Vesely)
- glsl: fix switch statement default case regressions (Tapani Pälli)
- st/dri: Fix driver loading if swrast isn't built (Aaron Watry)
- mesa/st: only convert AND(a, NOT(b)) into MAD when not using native integers (Ilia Mirkin)
- Remove XA state tracker support for Radeon (Marek Olšák)
- docs: Import 10.2.5 release notes, add news item. (Carl Worth)
- mesa/st: add support for dynamic ubo selection (Ilia Mirkin)
- i965: Delete stale "pre-gen4" comment in texture validation code. (Kenneth Graunke)
- i965: Delete sampler state structures. (Kenneth Graunke)
- i965: Replace sizeof(struct gen7_sampler_state) with the size itself. (Kenneth Graunke)
- i965: Drop sizeof(struct brw_sampler_state) from estimated prim size. (Kenneth Graunke)
- i965: Make BLORP use brw_emit_sampler_state(). (Kenneth Graunke)
- i965: Delete redundant sampler state dumping code. (Kenneth Graunke)
- i965: Make some brw_sampler_state.c functions static again. (Kenneth Graunke)
- i965: Stop using gen7_update_sampler_state; rm gen7_sampler_state.c. (Kenneth Graunke)
- i965: Make brw_update_sampler_state use 8 bits for LOD fields on Gen7+. (Kenneth Graunke)
- i965: Make brw_update_sampler_state() use brw_emit_sampler_state(). (Kenneth Graunke)
- i965: Introduce a function to emit a SAMPLER_STATE structure. (Kenneth Graunke)
- i965: Add const to upload_default_color's sampler parameter. (Kenneth Graunke)
- i965: Add #defines for SAMPLER_STATE fields. (Kenneth Graunke)
- i965: Convert wrap mode #defines to an enum. (Kenneth Graunke)
- i965: Delete gen7_upload_sampler_state_table and vtable mechanism. (Kenneth Graunke)
- i965: Make brw_upload_sampler_state_table handle Gen7+ as well. (Kenneth Graunke)
- i965: Shift brw_upload_sampler_state_table away from structures. (Kenneth Graunke)
- i965: Push computation for sampler state batch offsets up a level. (Kenneth Graunke)
- i965: Drop unused 'ss_index' parameter from gen7_update_sampler_state. (Kenneth Graunke)
- i965: Stop storing sdc_offset in brw_stage_state. (Kenneth Graunke)
- i965: Drop the degenerate brw_sampler_default_color structure. (Kenneth Graunke)
- i965: Write a better file comment for brw_sampler_state.c. (Kenneth Graunke)
- i965: Rename brw_wm_sampler_state.c to brw_sampler_state.c. (Kenneth Graunke)
- i965/blorp: Don't set min_mag_neq bit in Gen6 SAMPLER_STATE. (Kenneth Graunke)
- define GL_OES_standard_derivatives if extension is supported (Kevin Rogovin)
- llvmpipe: don't store number of layers per level (Roland Scheidegger)
- llvmpipe: integrate memory allocation into llvmpipe_texture_layout (Roland Scheidegger)
- llvmpipe: get rid of impossible code in alloc_image_data (Roland Scheidegger)
- i965/miptree: Layout 1D Array as 2D Array with height of 1 (Jordan Justen)
- r600g: Implement gpu_shader5 textureGather (Glenn Kennard)
- mesa: Add missing atomic buffer bindings and unbindings (Aditya Atluri)
- r600g/radeonsi: Prefer VRAM for CPU -> GPU streaming buffers (Michel Dänzer)
- r600g/radeonsi: Reduce or even drop special treatment of persistent mappings (Michel Dänzer)
- target-helpers: Do not build kms_dri on libdrm-less platforms. (Jon TURNEY)
- r600g: gpu_shader5 gl_SampleMaskIn support (Glenn Kennard)
- r600g: Implement gpu_shader5 integer ops (Glenn Kennard)
- r600g: Add IMUL_HI/UMUL_HI support (Glenn Kennard)
- r600g: Implement GL_ARB_texture_query_lod (Glenn Kennard)
- gbm: Log at least one dlerror() when we fail to open any drivers. (Eric Anholt)
- gbm: Fix a debug log message (Eric Anholt)
- gallium: Add a uif() helper function to complement fui() (Eric Anholt)
- glapi: Do not use backtrace on DragonFly. (Vinson Lee)
- gallivm: fix up out-of-bounds level when using conformant out-of-bound behavior (Roland Scheidegger)
- dri: Add a new capabilities for drivers that can't share buffers (Giovanni Campagna)
- gallium: Add a dumb drm/kms winsys backed swrast provider (Giovanni Campagna)
- Add support for swrast to the DRM EGL platform (Giovanni Campagna)
- st/gbm: don't segfault if the fail to create the screen (Emil Velikov)
- st/gbm: retrieve the driver-name via dd_driver_name() (Emil Velikov)
- glsl/glcpp: rename ERROR to ERROR_TOKEN to fix MSVC build (Brian Paul)
- configure: Don't override user -g or -O options for debug builds (Ian Romanick)
- glsl: Add flex options to eliminate the default rule (Carl Worth)
- glsl/glcpp: Add flex options to eliminate the default rule. (Carl Worth)
- glsl/glcpp: Combine the two rules matching any character (Carl Worth)
- glsl/glcpp: Alphabetize lists of start conditions (Carl Worth)
- glsl/glcpp: Add a catch-all rule for unexpected characters. (Carl Worth)
- glsl/glcpp: Treat carriage return as equivalent to line feed. (Carl Worth)
- glsl/glcpp: Add test for a multi-line comment within an #if 0 block (Carl Worth)
- glsl/glcpp: Test that macro parameters substitute immediately after periods (Carl Worth)
- glsl/glcpp: Add (non)-support for ++ and -- operators (Carl Worth)
- glsl/glcpp: Emit error for duplicate parameter name in function-like macro (Carl Worth)
- glsl/glcpp: Add an explanatory comment for "loc != NULL" check (Carl Worth)
- glsl/glcpp: Drop the HASH_ prefix from token names like HASH_IF (Carl Worth)
- glsl: Properly lex extra tokens when handling # directives. (Kenneth Graunke)
- glsl: Add an internal-error catch-all rule (Carl Worth)
- glsl/glcpp: Correctly parse directives with intervening comments (Carl Worth)
- glsl/glcpp: Rename HASH token to HASH_TOKEN (Carl Worth)
- glsl/glcpp: Don't use start-condition stack when switching to/from <DEFINE> (Carl Worth)
- glsl/glcpp: Add a -d/--debug option to the standalone glcpp program (Carl Worth)
- glsl/glcpp: Fix off-by-one error in column in first-line error messages (Carl Worth)
- glsl/glcpp: Minor tweak to wording of error message (Carl Worth)
- glsl/glcpp: Stop using a lexer start condition (<SKIP>) for token skipping. (Carl Worth)
- glsl/glcpp: Abstract a bit of common code for returning string tokens (Carl Worth)
- glsl/glcpp: Drop extra, final newline from most output (Carl Worth)
- glsl/glcpp: Add testing for EOF sans newline (and fix for <DEFINE>, <COMMENT>) (Carl Worth)
- glsl/glcpp: Remove some un-needed calls to NEWLINE_CATCHUP (Carl Worth)
- glsl/glcpp: Add support for comments between #define and macro identifier (Carl Worth)
- glsl/glcpp: Emit proper error for #define with a non-identifier (Carl Worth)
- glsl/glcpp: Add testing for directives preceded by a space (Carl Worth)
- glsl/glcpp: Fix to emit spaces following directives (Carl Worth)
- configure.ac: require libdrm_radeon 2.4.56 because of the Hawaii fix there (Marek Olšák)
- main/get_hash_params: Add GL_SAMPLE_SHADING_ARB (Jason Ekstrand)
- os_process.c: Add cygwin as an expected platform (Yaakov Selkowitz)
- xmlconfig: Use program_invocation_short_name when building for cygwin (Yaakov Selkowitz)
- docs: fix date typo: July 78 -> 18 (Brian Paul)
- svga: remove unneeded depth==1 assertion in svga_texture_view_surface() (Brian Paul)
- st/wgl: Clamp wglChoosePixelFormatARB's output nNumFormats to nMaxFormats. (José Fonseca)
- gallium/radeon: Add some Emacs .dir-locals.el files (Michel Dänzer)
- ilo: fix fb height of HiZ ops (Chia-I Wu)
- glapi: add indexed blend functions (GL 4.0) (Tapani Pälli)
- r600g,radeonsi: switch all occurences of array_size to util_max_layer (Marek Olšák)
- radeonsi: fix occlusion queries on Hawaii (Marek Olšák)
- winsys/radeon: fix vram_size overflow with Hawaii (Marek Olšák)
- radeonsi: fix a hang with streamout on Hawaii (Marek Olšák)
- radeonsi: fix a hang with instancing on Hawaii (Marek Olšák)
- gallium/util: add a helper for calculating primitive count from vertex count (Marek Olšák)
- radeonsi: fix CMASK and HTILE calculations for Hawaii (Marek Olšák)
- r600g,radeonsi: add debug flags which disable tiling (Marek Olšák)
- gallium: rename shader cap MAX_CONSTS to MAX_CONST_BUFFER_SIZE (Marek Olšák)
- r600g: switch SNORM conversion to DX and GLES behavior (Marek Olšák)
- util: Fix typo (Tom Stellard)
- ilo: correctly propagate resource renames to hardware (Chia-I Wu)
- ilo: add ilo_resource_get_bo() helper (Chia-I Wu)
- radeonsi: Use util_memcpy_cpu_to_le32() (Tom Stellard)
- util: Add util_memcpy_cpu_to_le32() v3 (Tom Stellard)
- clover: Add checks for image support to the image functions v2 (Tom Stellard)
- r600g/compute: Add debug information to promote and demote functions (Bruno Jiménez)
- r600g/compute: Add documentation to compute_memory_pool (Bruno Jiménez)
- ilo: unblock an inline write with a staging bo (Chia-I Wu)
- ilo: try unblocking a transfer with a staging bo (Chia-I Wu)
- ilo: enable persistent and coherent transfers (Chia-I Wu)
- ilo: drop ptr from ilo_transfer (Chia-I Wu)
- ilo: s/TRANSFER_MAP_UNSYNC/TRANSFER_MAP_GTT_UNSYNC/ (Chia-I Wu)
- ilo: drop unused context param from transfer functions (Chia-I Wu)
- ilo: tidy up transfer mapping/unmapping (Chia-I Wu)
- ilo: tidy up choose_transfer_method() (Chia-I Wu)
- ilo: free transfers with util_slab_free() (Chia-I Wu)
- clover: Add clUnloadPlatformCompiler. (EdB)
- clover: Add clCreateProgramWithBuiltInKernels. (EdB)
- glsl/cs: Add several GLSL compute shader variables (Jordan Justen)
- main/cs: Add additional compute shader constant values (Jordan Justen)
- glsl: No longer require ubo block index to be constant in ir_validate (Chris Forbes)
- glsl: Accept nonconstant array references in lower_ubo_reference (Chris Forbes)
- glsl: Convert uniform_block in lower_ubo_reference to ir_rvalue. (Chris Forbes)
- glsl: Mark entire UBO array active if indexed with non-constant. (Chris Forbes)
- glsl: Allow non-constant UBO array indexing with GLSL4/ARB_gpu_shader5. (Chris Forbes)
- ilo: simplify ilo_flush() (Chia-I Wu)
- r600g/compute: Defrag the pool at the same time as we grow it (Bruno Jiménez)
- r600g/compute: Try to use a temporary resource when growing the pool (Bruno Jiménez)
- freedreno: fix typo in gpu version check (Rob Clark)
- freedreno/ir3: split out shader compiler from a3xx (Rob Clark)
- freedreno/a3xx/compiler: rename ir3_shader to ir3 (Rob Clark)
- freedreno/a3xx/compiler: scheduler vs pred reg (Rob Clark)
- freedreno/a3xx/compiler: little cleanups (Rob Clark)
- freedreno/a3xx: enable/disable wa's based on patch-level (Rob Clark)
- freedreno/a3xx/compiler: make IR heap dyanmic (Rob Clark)
- r600g/compute: Fix singed/unsigned comparison compiler warnings. (Jan Vesely)
- clover: Query the device to see if images are supported (Tom Stellard)
- gallium: Add PIPE_CAP_COMPUTE_IMAGES_SUPPORTED (Tom Stellard)
- r600g/compute: Allow compute_memory_defrag to defragment between resources (Bruno Jiménez)
- r600g/compute: Allow compute_memory_move_item to move items between resources (Bruno Jiménez)
- gbm: Search LIBGL_DRIVERS_PATH if GBM_DRIVERS_PATH is not set (Dylan Baker)
- winsys/radeon: fix indentation (Jerome Glisse)
- Add an accelerated version of F_TO_I for x86_64 (Jason Ekstrand)
- i965/fs: Decide predicate/predicate_inverse outside of the for loop. (Matt Turner)
- i965/fs: Swap if/else conditions in SEL peephole. (Matt Turner)
- i965: Improve dead control flow elimination. (Matt Turner)
- nvc0/ir: support 2d constbuf indexing (Ilia Mirkin)
- gm107/ir: emit LDC subops (Ilia Mirkin)
- gk110/ir: emit load constant subop (Ilia Mirkin)
- mesa/st: add support for interpolate_at_* ops (Ilia Mirkin)
- nv50/ir: fix phi/union sources when their def has been merged (Ilia Mirkin)
- nv50/ir: fix hard-coded TYPE_U32 sized register (Ilia Mirkin)
- nvc0: mark shader header if fp64 is used (Ilia Mirkin)
- nv50/ir: keep track of whether the program uses fp64 (Ilia Mirkin)
- nvc0: make sure that the local memory allocation is aligned to 0x10 (Ilia Mirkin)
- mesa: add ARB_clear_texture.xml to file list, remove duplicate decls (Ilia Mirkin)
- ilo: check the tilings of imported handles (Chia-I Wu)
- ilo: clean up resource bo renaming (Chia-I Wu)
- ilo: share some code between {tex,buf}_create_bo (Chia-I Wu)
- ilo: use native 3-component vertex formats on GEN7.5+ (Chia-I Wu)
- ilo: allow for device-dependent format translation (Chia-I Wu)
- i965: Accelerate uploads of RGBA and BGRA GL_UNSIGNED_INT_8_8_8_8_REV textures (Jason Ekstrand)
- mesa: Fix the name in the error message (Ian Romanick)
- glsl: Fix some bad indentation (Ian Romanick)
- i965/fs: Set LastRT on the final FB write on Broadwell. (Kenneth Graunke)
- i965: Port INTEL_DEBUG=optimizer to the vec4 backend. (Kenneth Graunke)
- i965: Save the gl_shader_stage enum in backend_visitor. (Kenneth Graunke)
- i965: Don't print WE_normal in disassembly. (Kenneth Graunke)
- freedreno/a3xx/compiler: fix p0 (kill, etc) (Rob Clark)
- Revert "r600g/compute: Fix warnings" (Tom Stellard)
- radeon/llvm: fix formatting (Grigori Goronzy)
- radeon/llvm: enable unsafe math for graphics shaders (Grigori Goronzy)
- r600g/compute: Fix warnings (Tom Stellard)
- r600g: Use hardware sqrt instruction (Glenn Kennard)
- r600g/compute: Remove unneeded code from compute_memory_promote_item (Bruno Jiménez)
- r600g/compute: Quick exit if there's nothing to add to the pool (Bruno Jiménez)
- r600g/compute: Defrag the pool if it's necesary (Bruno Jiménez)
- r600g/compute: Add a function for defragmenting the pool (Bruno Jiménez)
- r600g/compute: Add a function for moving items in the pool (Bruno Jiménez)
- freedreno/a3xx: more vtx formats (Rob Clark)
- freedreno/a3xx/compiler: const file relative addressing (Rob Clark)
- freedreno/a3xx/compiler: move function (Rob Clark)
- freedreno/a3xx: add back a few stalls (Rob Clark)
- targets/dri: fix freedreno targets (Rob Clark)
- freedreno: update generated headers (Rob Clark)
- docs: Update GL3.txt and relnotes for GL_ARB_clear_texture (Neil Roberts)
- meta: Add a meta implementation of GL_ARB_clear_texture (Neil Roberts)
- meta: Add a state flag for the GL_DITHER (Neil Roberts)
- texstore: Add a generic implementation of GL_ARB_clear_texture (Neil Roberts)
- mesa/main: Add generic bits of ARB_clear_texture implementation (Neil Roberts)
- teximage: Add utility func for format/internalFormat compatibility check (Neil Roberts)
- mesa/main: add ARB_clear_texture entrypoints (Ilia Mirkin)
- r600g/radeonsi: Use write-combined CPU mappings of some BOs in GTT (Michel Dänzer)
- winsys/radeon: Use separate caching buffer managers for VRAM and GTT (Michel Dänzer)
- docs/GL3.txt: update status for ARB_compute_shader (Dave Airlie)
- mesa: Don't use memcpy() in _mesa_texstore() for float depth texture data (Anuj Phogat)
- i965/fs: Fix gl_SampleMask handling for SIMD16 on Gen8+. (Kenneth Graunke)
- i965/fs: Fix gl_SampleID for 2x MSAA and SIMD16 mode. (Kenneth Graunke)
- i965: Add missing persample_shading field to brw_wm_debug_recompile. (Kenneth Graunke)
- i965/disasm: Don't disassemble the URB complete field on Broadwell. (Kenneth Graunke)
- i965: Disable hex offset printing in disassembly. (Kenneth Graunke)
- i965/vec4: Use foreach_inst_in_block a couple more places. (Matt Turner)
- i965: Replace cfg instances with calls to calculate_cfg(). (Matt Turner)
- i965/cfg: Add a foreach_block_and_inst macro. (Matt Turner)
- i965: Add cfg to backend_visitor. (Matt Turner)
- radeonsi/compute: Add support scratch buffer support v2 (Tom Stellard)
- radeonsi/compute: Bump number of user sgprs for LLVM 3.5 (Tom Stellard)
- winsys/radeon:  Query the kernel for the number of SEs and SHs per SE (Tom Stellard)
- radeonsi/compute: Share COMPUTE_DBG macro with r600g (Tom Stellard)
- radeonsi: Read rodata from ELF and append it to the end of shaders (Tom Stellard)
- glsl: Fix bad indentation (Ian Romanick)
- i965: Silence unused parameter warning (Ian Romanick)
- i965: Silence 'comparison is always true' warning (Ian Romanick)
- i965: Silence many unused parameter warnings (Ian Romanick)
- configure.ac: Add LLVM patch version to error message. (Vinson Lee)
- main/format_pack: Fix a wrong datatype in pack_ubyte_R8G8_UNORM (Jason Ekstrand)
- docs: Import 10.2.4 release notes (Carl Worth)
- Add support for RGBA8 and RGBX8 textures in intel_texsubimage_tiled_memcpy (Jason Ekstrand)
- i965: Improve debug output in intelTexImage and intelTexSubimage (Jason Ekstrand)
- radeonsi: only update vertex buffers when they need updating (Marek Olšák)
- radeonsi: remove nr_vertex_buffers (Marek Olšák)
- radeonsi: move vertex buffer descriptors from IB to memory (Marek Olšák)
- radeonsi: add support for fine-grained sampler view updates (Marek Olšák)
- radeonsi: move si_set_sampler_views to si_descriptors.c (Marek Olšák)
- radeonsi: move sampler descriptors from IB to memory (Marek Olšák)
- radeonsi: implement ARB_draw_indirect (Marek Olšák)
- radeonsi: don't add info->start to the index buffer offset (Marek Olšák)
- radeonsi: use an SGPR instead of VGT_INDX_OFFSET (Marek Olšák)
- radeonsi: assume LLVM 3.4.2 is always present (Marek Olšák)
- configure.ac: require LLVM 3.4.2 for radeon (Marek Olšák)
- st/mesa,gallium: add a workaround for Unigine Heaven 4.0 and Valley 1.0 (Marek Olšák)
- glsl: add a mechanism to allow #extension directives in the middle of shaders (Marek Olšák)
- r600g: Implement GL_ARB_texture_gather (Glenn Kennard)
- i965: Fix z_offset computation in intel_miptree_unmap_depthstencil() (Anuj Phogat)
- Revert "i965: Extend compute-to-mrf pass to understand blocks of MOVs" (Anuj Phogat)
- i915: Fix up intelInitScreen2 for DRI3 (Adel Gadllah)
- mesa: Fix regression introduced by commit "mesa: fix packing of float texels to GL_SHORT/GL_BYTE". (Pavel Popov)
- nv50: fix build failure on m68k due to invalid struct alignment assumptions (Thorsten Glaser)
- clover: Call end_query before getting timestamp result v2 (Tom Stellard)
- glsl: handle a switch where default is in the middle of cases (Tapani Pälli)
- glsl: Make the tree rebalancer use vector_elements, not components(). (Kenneth Graunke)
- glsl: Guard against error_type in the tree rebalancer. (Kenneth Graunke)
- glsl: Make the tree rebalancer bail on matrix operands. (Kenneth Graunke)
- Revert "i965: Implement GL_PRIMITIVES_GENERATED with non-zero streams." (Kenneth Graunke)
- ilo: add some missing formats (Chia-I Wu)
- ilo: update and tailor the surface format table (Chia-I Wu)
- i965: Don't copy propagate abs into Broadwell logic instructions. (Kenneth Graunke)
- i965/fs: Use WE_all for gl_SampleID header register munging. (Kenneth Graunke)
- i965/fs: Set force_uncompressed and force_sechalf on samplepos setup. (Kenneth Graunke)
- i965: Set execution size to 8 for instructions with force_sechalf set. (Kenneth Graunke)
- nvc0: fix translate path for PRIM_RESTART_WITH_DRAW_ARRAYS (Christoph Bumiller)
- nvc0: add support for indirect drawing (Christoph Bumiller)
- nouveau: check if a fence has already been signalled (Ilia Mirkin)
- glsl: Don't declare variables in for-loop declaration. (Matt Turner)
- exec_list: Make various places use the new length() method. (Connor Abbott)
- exec_list: Add a function to give the length of a list. (Connor Abbott)
- exec_list: Add a prepend function. (Connor Abbott)
- mesa: Don't allow GL_TEXTURE_{LUMINANCE,INTENSITY}_* queries outside compat profile (Ian Romanick)
- mesa: Don't allow GL_TEXTURE_BORDER queries outside compat profile (Ian Romanick)
- mesa: Handle uninitialized textures like other textures in get_tex_level_parameter_image (Ian Romanick)
- i965/fs: Relax interference check in register coalescing. (Matt Turner)
- i965/fs: Perform CSE on sends-from-GRF rather than textures. (Matt Turner)
- glsl: Update expression types after rebalancing the tree. (Matt Turner)
- glsl: Add callback_leave to ir_hierarchical_visitor. (Matt Turner)
- i965: Initialize new chunks of realloc'd memory. (Matt Turner)
- radeon/llvm: Fix LLVM diagnostic error reporting (Tom Stellard)
- util/tgsi: Fix ureg_EMIT/ENDPRIM prototype. (José Fonseca)
- glapi: Use GetProcAddress instead of dlsym on Windows. (Vinson Lee)
- ilo: raise texture size limits (Chia-I Wu)
- ilo: move away from drm_intel_bo_alloc_tiled (Chia-I Wu)
- radeonsi: partially revert "switch descriptors to i32 vectors" (Marek Olšák)
- i965/vec4: Invalidate live intervals in opt_cse, not _local. (Matt Turner)
- i965/vec4: Move aeb list into opt_cse_local. (Matt Turner)
- i965/fs: Invalidate live intervals in opt_cse, not _local. (Matt Turner)
- i965/fs: Move aeb list into opt_cse_local. (Matt Turner)
- glsl: Fix aggregates with dynamic initializers. (Cody Northrop)
- Avoid mesa_dri_drivers import lib being installed (Jon TURNEY)
- i965/vec4: Silence warnings about unhandled interpolation ops (Chris Forbes)
- docs: Mark off ARB_gpu_shader5 interpolation functions for i965 (Chris Forbes)
- i965/fs: add support for ir_*_interpolate_at_* expressions (Chris Forbes)
- i965/fs: Skip channel expressions splitting for interpolation (Chris Forbes)
- i965/fs: add generator support for pixel interpolator query (Chris Forbes)
- i965: add low-level support for send to pixel interpolator (Chris Forbes)
- i965/disasm: add support for pixel interpolator messages (Chris Forbes)
- i965: Add message descriptor bit definitions for pixel interpolator (Chris Forbes)
- i965/disasm: Disassemble indirect sends more properly (Chris Forbes)
- i965: Avoid crashing while dumping vec4 insn operands (Chris Forbes)
- i965: Fix two broken asserts in brw_eu_emit (Chris Forbes)
- glsl: add new interpolateAt* builtin functions (Chris Forbes)
- glsl: add new expression types for interpolateAt* (Chris Forbes)
- allow builtin functions to require parameters to be shader inputs (Chris Forbes)
- radeonsi: rename definitions of shader limits (Marek Olšák)
- radeonsi: switch descriptors to i32 vectors (Marek Olšák)
- radeonsi: properly implement texture opcodes that take an offset (Marek Olšák)
- radeonsi: fix texture fetches with derivatives for 1DArray and 3D textures (Marek Olšák)
- radeonsi: fix samplerCubeShadow with bias (Marek Olšák)
- st/mesa: fix samplerCubeShadow with bias (Marek Olšák)
- mesa: fix crash in st/mesa after deleting a VAO (Marek Olšák)

* Fri Jul 11 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.3-0.devel.1.f381c27c548aa28b003c8e188f5d627ab4105f76
- Rebase to 'master' branch (f381c27c548aa28b003c8e188f5d627ab4105f76 commit)

* Fri Jul 11 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2.3-1.20140711
- 10.2.3 upstream release

* Mon Jul  7 2014 Peter Robinson <pbrobinson@fedoraproject.org> 10.2.2-4.20140625
- Build aarch64 options the same as ARMv7
- Fix PPC conditionals

* Fri Jul 04 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2.2-3.20140625
- Fix up intelInitScreen2 for DRI3 (RHBZ #1115323) (patch from drago01)

* Fri Jun 27 2014 Dave Airlie <airlied@redhat.com> 10.2.2-2.20140625
- add dri3 gnome-shell startup fix from Jasper.

* Wed Jun 25 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2.2-1.20140625
- 10.2.2 upstream release

* Wed Jun 11 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2.1-2.20140608
- drop radeonsi llvm hack

* Sun Jun 08 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2.1-1.20140608
- 10.2.1 upstream release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.2-0.11.rc5.20140531
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jun 04 2014 Dan Horák <dan[at]danny.cz> - 10.2-0.10.rc5.20140531
- fix build without hardware drivers

* Sat May 31 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2-0.9.rc5.20140531
- 10.2-rc5 upstream release

* Wed May 28 2014 Brent Baude <baude@us.ibm.com> - 10.2-0.8.rc4.20140524
- Removing ppc64le arch from with_llvm

* Wed May 28 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2-0.7.rc4.20140524
- i915: add a missing NULL pointer check (RHBZ #1100967)

* Sat May 24 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2-0.6.rc4.20140524
- 10.2-rc4 upstream release
- add back updated radeonsi hack for LLVM

* Sat May 17 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2-0.5.rc3.20140517
- 10.2-rc3 upstream release

* Sat May 10 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2-0.4.rc2.20140510
- 10.2-rc2 upstream release
- drop radeonsi hack for LLVM

* Tue May 06 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2-0.3.rc1.20140505
- Move gallium-pipe to the correct sub-package (RHBZ #1094588) (kwizart)
- Move egl_gallium.so to the correct location (RHBZ #1094588) (kwizart)
- Switch from with to enable for llvm shared libs (kwizart)

* Mon May 05 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2-0.2.rc1.20140505
- Enable gallium-egl (needed by freedreeno) (RHBZ #1094199) (kwizart)

* Mon May 05 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2-0.1.rc1.20140505
- Enable omx on x86 and arm (RHBZ #1094199) (kwizart)
- Split _with_xa from _with_vmware (RHBZ #1094199) (kwizart)
- Add _with_xa when arch is arm and _with_freedreeno (RHBZ #1094199) (kwizart)

* Mon May 05 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.2-0.rc1.20140505
- 10.2-rc1 upstream release

* Wed Apr 30 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.1.1-3.20140430
- Update to today snapshot
- apply as downstream patches for reporting GPU max frequency on r600 (FD.o #73511)

* Sat Apr 19 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.1.1-2.20140419
- fix buildrequires llvm 3.4-5 to 3.4-6, because 3.4-5 is not available for F20

* Sat Apr 19 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.1.1-1.20140419
- 10.1.1 upstream release

* Tue Apr 15 2014 Adam Jackson <ajax@redhat.com> 10.1-6.20140305
- Disable DRI3 in F20, it requires libxcb bits we haven't backported.

* Wed Mar 26 2014 Adam Jackson <ajax@redhat.com> 10.1-5.20140305
- Initial ppc64le enablement (no hardware drivers or vdpau yet)

* Fri Mar 21 2014 Adam Jackson <ajax@redhat.com> 10.1-4.20140305
- mesa: Don't optimize out glClear if drawbuffer size is 0x0 (fdo #75797)

* Wed Mar 19 2014 Dave Airlie <airlied@redhat.com> 10.1-3.20140305
- rebuild against backported llvm 3.4-5 for radeonsi GL 3.3 support.

* Wed Mar 12 2014 Dave Airlie <airlied@redhat.com> 10.1-2.20140305
- disable r600 llvm compiler (upstream advice)

* Wed Mar 05 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.1-1.20140305
- mesa: Bump version to 10.1 (final) (Ian Romanick)
- glx/dri2: fix build failure on HURD (Julien Cristau)
- i965: Validate (and resolve) all the bound textures. (Chris Forbes)
- i965: Widen sampler key bitfields for 32 samplers (Chris Forbes)

* Sat Mar 01 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.1-0.rc3.20140301
- 10.1-rc3

* Tue Feb 25 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.1-0.rc2.20140225
- really 10.1-rc2

* Sat Feb 22 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.1-0.rc2.20140222
- 10.1-rc2

* Sat Feb 08 2014 Adel Gadllah <adel.gadllah@gmail.com> - 10.1-0.rc1.20140208
- 10.1rc1
- Drop upstreamed patches

* Thu Feb 06 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.0.3-1.20140206
- 10.0.3 upstream release

* Tue Feb 04 2014 Kyle McMartin <kyle@redhat.com> - 10.0.2-6.20140118
- Fix accidentally inverted logic that meant radeonsi_dri.so went missing
  on all architectures instead of just ppc and s390. Sorry!

* Sun Feb 02 2014 Kyle McMartin <kyle@redhat.com> - 10.0.2-5.20140118
- Fix a thinko in previous commit wrt libdrm_nouveau2.

* Sun Feb 02 2014 Kyle McMartin <kyle@redhat.com> - 10.0.2-4.20140118
- Fix up building drivers on AArch64, enable LLVM there.
- Eliminate some F17 cruft from the spec, since we don't support it anymore.
- Conditionalize with_radeonsi on with_llvm instead of ppc,s390 && >F-17.
- Conditionalize libvdpau_radeonsi.so.1* on with_radeonsi instead of simply
  with_llvm to fix a build failure on AArch64.

* Sun Jan 19 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 10.0.2-3.20140118
- Enable OpenCL (RHBZ #887628)
- Enable r600 llvm compiler (RHBZ #1055098)

* Fri Dec 20 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 9.2.5-1.20131220
- 9.2.5 upstream release

* Fri Dec 13 2013 Dave Airlie <airlied@redhat.com> 9.2.4-2.20131128
- backport the GLX_MESA_copy_sub_buffer from upstream for cogl

* Thu Nov 28 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 9.2.4-1.20131128
- 9.2.4 upstream release

* Thu Nov 14 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 9.2.3-1.20131114
- 9.2.3 upstream release

* Wed Nov 13 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 9.2.2-1.20131113
- 9.2.2 upstream release + fixes from git 9.2 branch

* Thu Sep 19 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 9.2-1.20130919
- Today's git snap of 9.2 branch
- [NVE4] Fix crashing games when set AA to x2 on GTX760
- (freedesktop 68665 rhbz 1001714 1001698 1001740 1004674)

* Mon Sep 02 2013 Dave Airlie <airlied@redhat.com> 9.2-1.20130902
- 9.2 upstream release + fixes from git branch

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.2-0.15.20130723
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Adam Jackson <ajax@redhat.com> 9.2-0.14.20130723
- Today's git snap of 9.2 branch

* Sun Jul 14 2013 Kyle McMartin <kyle@redhat.com> 9.2-0.13.20130610
- Use LLVM::MCJIT on ARM and AArch64.

* Mon Jun 17 2013 Adam Jackson <ajax@redhat.com> 9.2-0.12.20130610
- Re-enable hardware float support (#975204)

* Mon Jun 17 2013 Adam Jackson <ajax@redhat.com> 9.2-0.11.20130610
- Fix evergreen on big-endian

* Wed Jun 12 2013 Adam Jackson <ajax@redhat.com> 9.2-0.10.20130610
- Fix s390x build
- Fold khrplatform-devel in to libEGL-devel

* Tue Jun 11 2013 Adam Jackson <ajax@redhat.com> 9.2-0.9.20130610
- 0001-Revert-i965-Disable-unused-pipeline-stages-once-at-s.patch: Fix some
  hangs on ivb+

* Mon Jun 10 2013 Adam Jackson <ajax@redhat.com> 9.2-0.8.20130610
- Today's git snap

* Tue May 28 2013 Adam Jackson <ajax@redhat.com> 9.2-0.7.20130528
- Today's git snap

* Sun May 19 2013 Peter Robinson <pbrobinson@fedoraproject.org> 9.2-0.6.20130514
- Update the name of the freedreno driver

* Fri May 17 2013 Adam Jackson <ajax@redhat.com> 9.2-0.5.20130514
- Fix build issues on ppc32

* Thu May 16 2013 Adam Jackson <ajax@redhat.com> 9.2-0.4.20130514
- Fix yet more build issues on s390{,x}

* Wed May 15 2013 Adam Jackson <ajax@redhat.com> 9.2-0.3.20130514
- Fix build ordering issue on s390x

* Wed May 15 2013 Adam Jackson <ajax@redhat.com> 9.2-0.2.20130514
- Fix filesystem for with_hardware == 0

* Tue May 14 2013 Adam Jackson <ajax@redhat.com> 9.2-0.1.20130514
- Today's git snap
- Revert to swrast on ppc32 and s390 since llvm doesn't actually work
- Build freedreno on arm
- Drop snb hang workaround (upstream 1dfea559)
- Rename filesystem package

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
