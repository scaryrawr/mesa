# Choose one and only one.
%define build_fc	1
%define build_rhel	0

#-- DRI Build Configuration ------------------------------------------
# NOTE: Enable DRI on PPC for Fedora Core Mac users, but disable on
# RHEL for improved stability, as DRI isn't really that important
# on server platforms.
%if %{build_fc}
%define with_dri_ppc 1
%endif
%if %{build_rhel}
%define with_dri_ppc 0
%endif

# Architechture specific configuration
%ifarch %{ix86}
%define with_dri 1
%define dri_target linux-dri-x86
%endif

%ifarch x86_64
%define with_dri 1
%define dri_target linux-dri-x86-64
%endif

%ifarch ia64 alpha sparc sparc64
%define with_dri 1
%define dri_target linux-dri
%endif

%ifarch ppc
%define with_dri %{with_dri_ppc}
%define dri_target linux-dri-ppc
%endif

# Define arches to make with_dri disabled by default
%ifarch ppc64 s390 s390x
%define with_dri 0
%define dri_target linux-indirect
%endif

#-- END DRI Build Configuration ------------------------------------------

Summary: Mesa graphics libraries
Name: mesa
Version: 6.5.1
Release: 3%{?dist}
License: MIT/X11
Group: System Environment/Libraries
URL: http://www.mesa3d.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0: http://internap.dl.sourceforge.net/sourceforge/mesa3d/MesaLib-6.5.1.tar.bz2
Source1: http://internap.dl.sourceforge.net/sourceforge/mesa3d/MesaDemos-6.5.1.tar.bz2
Source12: redhat-mesa-source-filelist-generator

# Patches 0-9 reserved for mesa Makefiles/config fixes
Patch0: mesa-6.5.1-build-config.patch
Patch4: mesa-6.5-dont-libglut-me-harder-ok-thx-bye.patch

Patch18: mesa-6.5.1-selinux-awareness.patch

# General patches from upstream go here:

BuildRequires: pkgconfig
%if %{with_dri}
BuildRequires: libdrm-devel >= 2.0.1-4
%endif
BuildRequires: libXxf86vm-devel
BuildRequires: expat-devel
BuildRequires: xorg-x11-proto-devel >= 7.1-8
BuildRequires: makedepend
BuildRequires: libselinux-devel
BuildRequires: libXext-devel

%description
Mesa

#-- libGL ------------------------------------------------------------
%package libGL
Summary: Mesa libGL runtime libraries and DRI drivers
Group: System Environment/Libraries

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
# NOTE: This libGL virtual provide is intentionally non-versioned, and is
# intended to be used as a generic dependency in other packages which require
# _any_ implementation and version of libGL.  If a particular software
# package requires a specific GL feature which is unique to Mesa, or to
# another GL implementation, then by definition that software is not OpenGL
# implementation agnostic, and should not be using these virtual provides.
# Instead, they should use "Requires: mesa-libGL-devel >= version-release"
# or substitute another implementation as appropriate.
Provides: libGL

# libGL used to be in Mesa package in RHL 6.x, 7.[0-2], RHEL 2.1
Obsoletes: Mesa
# libGL moved to XFree86-libs for RHL 7.3
Obsoletes: XFree86-libs
# libGL moved to XFree86-Mesa-libGL for RHL 8.0, 9, FC1, RHEL 3
Obsoletes: XFree86-Mesa-libGL
# libGL moved to xorg-x11-Mesa-libGL for FC[2-4], RHEL4
Obsoletes: xorg-x11-Mesa-libGL
# Conflict with the xorg-x11-libs too, just to be safe for file conflicts
Obsoletes: xorg-x11-libs

%description libGL
Mesa libGL runtime libraries and DRI drivers.
#-- libGL ------------------------------------------------------------
%package libGL-devel
Summary: Mesa libGL development package
Group: Development/Libraries
Requires: mesa-libGL = %{version}-%{release}
Requires: libX11-devel

# NOTE: This libGL virtual provide is intentionally non-versioned, and is
# intended to be used as a generic dependency in other packages which require
# _any_ implementation and version of libGL.  If a particular software
# package requires a specific GL feature which is unique to Mesa, or to
# another GL implementation, then by definition that software is not OpenGL
# implementation agnostic, and should not be using these virtual provides.
# Instead, they should use "Requires: mesa-libGL-devel >= version-release"
# or substitute another implementation as appropriate.
Provides: libGL-devel

# libGL devel files were in Mesa-devel package in RHL 6.x, 7.[0-2], RHEL 2.1
Obsoletes: Mesa-devel
# libGL devel files moved to XFree86-devel for RHL 7.3, 8.0, 9, FC1, RHEL 3
Obsoletes: XFree86-devel
# libGL devel files moved to xorg-x11-devel for FC2, FC3, FC4
Obsoletes: xorg-x11-devel

%description libGL-devel
Mesa libGL development package
#-- libGLU -----------------------------------------------------------
%package libGLU
Summary: Mesa libGLU runtime library
Group: System Environment/Libraries

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

# NOTE: This libGLU virtual provide is intentionally non-versioned, and is
# intended to be used as a generic dependency in other packages which require
# _any_ implementation and version of libGLU.  If a particular software
# package requires a specific GLU feature which is unique to Mesa, or to
# another GLU implementation, then by definition that software is not GLU
# implementation agnostic, and should not be using these virtual provides.
# Instead, they should use "Requires: mesa-libGLU-devel >= version-release"
# or substitute another implementation as appropriate.
Provides: libGLU

# libGLU used to be in Mesa package in RHL 6.x, 7.[0-2], RHEL 2.1
Obsoletes: Mesa
# libGLU moved to XFree86-libs for RHL 7.3
Obsoletes: XFree86-libs
# libGLU moved to XFree86-Mesa-libGLU for RHL 8.0, 9, FC1, RHEL 3
Obsoletes: XFree86-Mesa-libGLU
# libGLU moved to xorg-x11-Mesa-libGLU for FC[2-4], RHEL4
Obsoletes: xorg-x11-Mesa-libGLU
# Obsolete xorg-x11-libs too, just to be safe
Obsoletes: xorg-x11-libs

%description libGLU
Mesa libGLU runtime library
#-- libGLU-devel -----------------------------------------------------
%package libGLU-devel
Summary: Mesa libGLU development package
Group: Development/Libraries
Requires: mesa-libGLU = %{version}-%{release}
Requires: libGL-devel

# NOTE: This libGLU virtual provide is intentionally non-versioned, and is
# intended to be used as a generic dependency in other packages which require
# _any_ implementation and version of libGLU.  If a particular software
# package requires a specific GLU feature which is unique to Mesa, or to
# another GLU implementation, then by definition that software is not GLU
# implementation agnostic, and should not be using these virtual provides.
# Instead, they should use "Requires: mesa-libGLU-devel >= version-release"
# or substitute another implementation as appropriate.
Provides: libGLU-devel

# libGLU devel files were in Mesa-devel package in RHL 6.x, 7.[0-2], RHEL 2.1
Obsoletes: Mesa-devel
# libGLU devel files moved to XFree86-devel for RHL 7.3, 8.0, 9, FC1, RHEL 3
Obsoletes: XFree86-devel
# libGLU devel files moved to xorg-x11-devel for FC2, FC3, FC4
Obsoletes: xorg-x11-devel

%description libGLU-devel
Mesa libGLU development package

#-- libOSMesa -----------------------------------------------------------
%package libOSMesa
Summary: Mesa offscreen rendering libraries
Group: System Environment/Libraries

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

Provides: libOSMesa

%description libOSMesa
Mesa offscreen rendering libraries

#-- libOSMesa-devel -----------------------------------------------------
%package libOSMesa-devel
Summary: Mesa offscreen rendering development package
Group: Development/Libraries
Requires: mesa-libOSMesa = %{version}-%{release}

%description libOSMesa-devel
Mesa offscreen rendering development package

#-- source -----------------------------------------------------------
%package source
Summary: Mesa source code required to build X server
Group: Development/Libraries

%description source
The mesa-source package provides the minimal source code needed to
build DRI enabled X servers, etc.

#-- glx-utils --------------------------------------------------------
%package -n glx-utils
Summary: GLX utilities
Group: Development/Libraries

%description -n glx-utils
The glx-utils package provides the glxinfo and glxgears utilities.

#-- prep -------------------------------------------------------------
%prep
%setup -q -n Mesa-%{version} -b1
# Copy Red Hat Mesa build/install simplificomplication scripts into build dir.
install -m 755 %{SOURCE12} ./

%patch0 -p1 -b .build-config
%patch4 -p0 -b .dont-libglut-me-harder-ok-thx-bye

%patch18 -p1 -b .selinux-awareness

# WARNING: The following files are copyright "Mark J. Kilgard" under the GLUT
# license and are not open source/free software, so we remove them.
rm -f include/GL/uglglutshapes.h

#-- Build ------------------------------------------------------------
%build
export OPT_FLAGS="$RPM_OPT_FLAGS"
export DRI_DRIVER_DIR="%{_libdir}/dri"
export LIB_DIR=%{_lib}

mkdir preserve

for t in osmesa osmesa16 osmesa32; do
    echo "Building $t"
    make linux-$t
    mv %{_lib}/* preserve
    make -s realclean
done

echo "Building %{dri_target}"
make %{dri_target}
make -C progs/xdemos glxgears glxinfo
mv preserve/* %{_lib}
ln -s libOSMesa.so.6 %{_lib}/libOSMesa.so 
ln -s libOSMesa16.so.6 %{_lib}/libOSMesa16.so
ln -s libOSMesa32.so.6 %{_lib}/libOSMesa32.so

#-- Install ----------------------------------------------------------
%install
rm -rf $RPM_BUILD_ROOT

# The mesa build system is broken beyond repair.  The lines below just
# handpick and manually install the parts we want.

install -d $RPM_BUILD_ROOT%{_includedir}/GL
install -m 644 include/GL/*.h $RPM_BUILD_ROOT%{_includedir}/GL

install -d $RPM_BUILD_ROOT%{_libdir}
cp -d -f %{_lib}/lib* $RPM_BUILD_ROOT%{_libdir}

install -d $RPM_BUILD_ROOT%{_bindir}
install -m 0755 progs/xdemos/glxgears $RPM_BUILD_ROOT%{_bindir}
install -m 0755 progs/xdemos/glxinfo $RPM_BUILD_ROOT%{_bindir}

%if %{with_dri}
install -d $RPM_BUILD_ROOT%{_libdir}/dri
for f in i810 i915 i965 mga r128 r200 r300 radeon savage sis tdfx unichrome; do
    so=%{_lib}/${f}_dri.so
    test -e $so && install -m 0755 $so  $RPM_BUILD_ROOT%{_libdir}/dri
done
%endif

# Run custom source filelist generator script, passing it a prefix
%define mesa_source_filelist mesa-source-rpm-filelist.lst
%define mesasourcedir %{_datadir}/mesa/source

./redhat-mesa-source-filelist-generator $RPM_BUILD_ROOT %{mesasourcedir}

#-- Clean ------------------------------------------------------------
%clean
rm -rf $RPM_BUILD_ROOT

#-- Check ------------------------------------------------------------
%check

%post libGL -p /sbin/ldconfig
%postun libGL -p /sbin/ldconfig
%post libGLU -p /sbin/ldconfig
%postun libGLU -p /sbin/ldconfig
%post libOSMesa -p /sbin/ldconfig
%postun libOSMesa -p /sbin/ldconfig

%files libGL
%defattr(-,root,root,-)
%{_libdir}/libGL.so.1
%{_libdir}/libGL.so.1.2

%if %{with_dri}
# DRI modules
%dir %{_libdir}/dri
# We only install drivers that get build and are in our white list so
# we can just glob here.
%{_libdir}/dri/*_dri.so
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
%{_includedir}/GL/glfbdev.h
%{_includedir}/GL/glx.h
%{_includedir}/GL/glx_mangle.h
%{_includedir}/GL/glxext.h
%{_includedir}/GL/mesa_wgl.h
%{_includedir}/GL/mglmesa.h
%{_includedir}/GL/svgamesa.h
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
%{_libdir}/libGLU.so.1.3.*

%files libGLU-devel
%defattr(-,root,root,-)
%{_libdir}/libGLU.so
%{_includedir}/GL/glu.h
%{_includedir}/GL/glu_mangle.h

%files libOSMesa
%defattr(-,root,root,-)
%{_libdir}/libOSMesa.so.6
%{_libdir}/libOSMesa.so.6.5.1
%{_libdir}/libOSMesa16.so.6
%{_libdir}/libOSMesa16.so.6.5.1
%{_libdir}/libOSMesa32.so.6
%{_libdir}/libOSMesa32.so.6.5.1

%files libOSMesa-devel
%defattr(-,root,root,-)
%{_includedir}/GL/osmesa.h
%{_libdir}/libOSMesa.so
%{_libdir}/libOSMesa16.so
%{_libdir}/libOSMesa32.so

%files source -f mesa-source-rpm-filelist.lst
%defattr(-,root,root,-)

%files -n glx-utils
%defattr(-,root,root,-)
%{_bindir}/glxgears
%{_bindir}/glxinfo

%changelog
* Wed Sep 20 2006 Kristian Høgsberg <krh@redhat.com> - 6.5.1-3.fc6
- Bump xorg-x11-proto-devel BuildRequires to 7.1-8 so we pick up the
  latest GLX_EXT_texture_from_pixmap opcodes.

* Wed Sep 20 2006 Kristian Høgsberg <krh@redhat.com> - 6.5.1-2.fc6
- Remove mesa-6.5-drop-static-inline.patch.

* Tue Sep 19 2006 Kristian Høgsberg <krh@redhat.com> 6.5.1-1.fc6
- Bump to 6.5.1 final release.
- Drop libGLw subpackage, it is now in Fedora Extras (#188974) and
  tweak mesa-6.5.1-build-config.patch to not build libGLw.
- Drop mesa-6.5.1-r300-smooth-line.patch, the smooth line fallback can
  now be prevented by enabling disable_lowimpact_fallback in
  /etc/drirc.
- Drop mesa-6.4.1-radeon-use-right-texture-format.patch, now upstream.
- Drop mesa-6.5-drop-static-inline.patch, workaround no longer necessary.

* Thu Sep  7 2006 Kristian Høgsberg <krh@redhat.com>
- Drop unused mesa-modular-dri-dir.patch.

* Tue Aug 29 2006 Kristian Høgsberg <krh@redhat.com> - 6.5.1-0.rc2.fc6
- Rebase to 6.5.1 RC2.
- Get rid of redhat-mesa-driver-install and redhat-mesa-target helper
  scripts and clean up specfile a bit.

* Mon Aug 28 2006 Kristian Høgsberg <krh@redhat.com> - 6.5.1-0.rc1.2.fc6
- Drop upstreamed patches mesa-6.5-texture-from-pixmap-fixes.patch and
  mesa-6.5-tfp-fbconfig-attribs.patch and fix
  mesa-6.4.1-radeon-use-right-texture-format.patch to not break 16bpp
  transparency.

* Fri Aug 25 2006 Adam Jackson <ajackson@redhat.com> - 6.5.1-0.rc1.1.fc6
- mesa-6.5.1-build-config.patch: Add i965 to x86-64 config.

* Wed Aug 23 2006 Kristian Høgsberg <krh@redhat.com> - 6.5.1-0.rc1.fc6
- Bump to 6.5.1 RC1.

* Tue Aug 22 2006 Kristian Høgsberg <krh@redhat.com> 6.5-26.20060818cvs.fc6
- Pull the vtxfmt patch into the selinux-awareness patch, handle exec
  mem heap init failure correctly by releasing mutex.

* Tue Aug 22 2006 Adam Jackson <ajackson@redhat.com> 6.5-25.20060818cvs.fc6
- mesa-6.5.1-r300-smooth-line.patch: Added, fakes smooth lines with aliased
  lines on R300+ cards, makes Google Earth tolerable.
- mesa-6.5-force-r300.patch: Resurrect.

* Tue Aug 22 2006 Adam Jackson <ajackson@redhat.com> 6.5-24.20060818cvs.fc6
- mesa-6.5.1-radeon-vtxfmt-cleanup-properly.patch: Fix a segfault on context
  destruction when selinux is enabled.

* Mon Aug 21 2006 Adam Jackson <ajackson@redhat.com> 6.5-23.20060818cvs.fc6
- redhat-mesa-driver-install: Reenable installing the tdfx driver. (#203295)

* Fri Aug 18 2006 Adam Jackson <ajackson@redhat.com> 6.5-22.20060818cvs.fc6
- Update to pre-6.5.1 snapshot.
- Re-add libOSMesa{,16,32}. (#186366)
- Add BuildReq: on libXp-devel due to openmotif header insanity.

* Sun Aug 13 2006 Florian La Roche <laroche@redhat.com> 6.5-21.fc6
- fix one Requires: to use the correct mesa-libGLw name

* Thu Jul 27 2006 Mike A. Harris <mharris@redhat.com> 6.5-20.fc6
- Conditionalized libGLw inclusion with new with_libGLw macro defaulting
  to 1 (enabled) for now, however since nothing in Fedora Core uses libGLw
  anymore, we will be transitioning libGLw to an external package maintained
  in Fedora Extras soon.

* Wed Jul 26 2006 Kristian Høgsberg <krh@redhat.com> 6.5-19.fc5.aiglx
- Build for fc5 aiglx repo.

* Tue Jul 25 2006 Adam Jackson <ajackson@redhat.com> 6.5-19.fc6
- Disable TLS dispatch, it is selinux-hostile.

* Tue Jul 25 2006 Adam Jackson <ajackson@redhat.com> 6.5-18.fc6
- mesa-6.5-fix-glxinfo-link.patch: lib64 fix.

* Tue Jul 25 2006 Adam Jackson <ajackson@redhat.com> 6.5-17.fc6
- mesa-6.5-fix-linux-indirect-build.patch: Added.
- mesa-6.5-fix-glxinfo-link.patch: Added.
- Build libOSMesa never instead of inconsistently; to be fixed later.
- Updates to redhat-mesa-target:
  - Always select linux-indirect when not building for DRI
  - Enable DRI to be built on PPC64 (still disabled in the spec file though)
  - MIT licence boilerplate

* Tue Jul 25 2006 Mike A. Harris <mharris@redhat.com> 6.5-16.fc6
- Remove glut-devel dependency, as nothing actually uses it that we ship.
- Added mesa-6.5-dont-libglut-me-harder-ok-thx-bye.patch to prevent libglut
  and other libs from being linked into glxgears/glxinfo even though they
  are not actually used.  This was the final package linking to freeglut in
  Fedora Core, blocking freeglut from being moved to Extras.
- Commented all of the virtual provides in the spec file to document clearly
  how they should be used by other developers in specifying build and runtime
  dependencies when packaging software which links to libGL, libGLU, and
  libGLw. (#200069)

* Mon Jul 24 2006 Adam Jackson <ajackson@redhat.com> 6.5-15.fc6
- Attempt to add selinux awareness; check if we can map executable memory
  and fail softly if not.  Removes the need for allow_execmem from huge
  chunks of the desktop.
- Disable the r300 gart fix for not compiling.

* Mon Jul 24 2006 Kristian Høgsberg <krh@redhat.com> 6.5-14.fc6
- Add mesa-6.5-r300-free-gart-mem.patch to make r300 driver free gart
  memory on context destroy.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 6.5-13.1.fc6
- rebuild

* Wed Jul 05 2006 Mike A. Harris <mharris@redhat.com> 6.5-13.fc6
- Added mesa-6.5-fix-opt-flags-bug197640.patch as 2nd attempt to fix OPT_FLAGS
  for (#197640).
- Ensure that redhat-mesa-driver-install creates $DRIMODULE_DESTDIR with
  mode 0755.

* Wed Jul 05 2006 Mike A. Harris <mharris@redhat.com> 6.5-12.fc6
- Maybe actually, you know, apply the mesa-6.5-glx-use-tls.patch as that might
  help to you know, actually solve the problem.  Duh.
- Use {dist} tag in Release field now.

* Wed Jul 05 2006 Mike A. Harris <mharris@redhat.com> 6.5-11
- Added mesa-6.5-glx-use-tls.patch to hopefully get -DGLX_USE_TLS to really
  work this time due to broken upstream linux-dri-* configs. (#193979)
- Pass RPM_OPT_FLAGS via OPT_FLAGS instead of via CFLAGS also for (#193979)

* Mon Jun 19 2006 Mike A. Harris <mharris@redhat.com> 6.5-10
- Bump libdrm-devel dep to trigger new ExclusiveArch test with the new package.
- Use Fedora Extras style BuildRoot tag.
- Added "Requires(post): /sbin/ldconfig" and postun to all runtime lib packages.

* Mon Jun 12 2006 Kristian Høsberg <krh@redhat.com> 6.5-9
- Add mesa-6.5-fix-pbuffer-dispatch.patch to fix pbuffer marshalling code.

* Mon May 29 2006 Kristian Høgsberg <krh@redhat.com> 6.5-8
- Bump for rawhide build.

* Mon May 29 2006 Kristian Høgsberg <krh@redhat.com> 6.5-7
- Update mesa-6.5-texture-from-pixmap-fixes.patch to include new
  tokens and change tfp functions to return void.  Yes, a new mesa
  snapshot would be nice.

* Wed May 17 2006 Mike A. Harris <mharris@redhat.com> 6.5-6
- Add "BuildRequires: makedepend" for bug (#191967)

* Tue Apr 11 2006 Kristian Høgsberg <krh@redhat.com> 6.5-5
- Bump for fc5 build.

* Tue Apr 11 2006 Adam Jackson <ajackson@redhat.com> 6.5-4
- Disable R300_FORCE_R300 hack for wider testing.

* Mon Apr 10 2006 Kristian Høgsberg <krh@redhat.com> 6.5-3
- Add mesa-6.5-noexecstack.patch to prevent assembly files from making
  libGL.so have executable stack.

* Mon Apr 10 2006 Kristian Høgsberg <krh@redhat.com> 6.5-2
- Bump for fc5 build.
- Bump libdrm requires to 2.0.1.

* Sat Apr 01 2006 Kristian Høgsberg <krh@redhat.com> 6.5-1
- Update to mesa 6.5 snapshot.
- Use -MG for generating deps and some files are not yet symlinked at
  make depend time.
- Drop mesa-6.4.2-dprintf-to-debugprintf-for-bug180122.patch and
  mesa-6.4.2-xorg-server-uses-bad-datatypes-breaking-AMD64-fdo5835.patch
  as these are upstream now.
- Drop mesa-6.4.1-texture-from-drawable.patch and add
  mesa-6.5-texture-from-pixmap-fixes.patch.
- Update mesa-modular-dri-dir.patch to apply.
- Widen libGLU glob.
- Reenable r300 driver install.
- Widen libOSMesa glob.
- Go back to patching config/linux-dri, add mesa-6.5-build-config.patch,
  drop mesa-6.3.2-build-configuration-v4.patch.
- Disable sis dri driver for now, only builds on x86 and x86-64.

* Fri Mar 24 2006 Kristian Høgsberg <krh@redhat.com> 6.4.2-7
- Set ARCH_FLAGS=-DGLX_USE_TLS to enable TLS for GL contexts.

* Wed Mar 01 2006 Karsten Hopp <karsten@redhat.de> 6.4.2-6
- Buildrequires: libXt-devel (#183479)

* Sat Feb 25 2006 Mike A. Harris <mharris@redhat.com> 6.4.2-5
- Disable the expeimental r300 DRI driver, as it has turned out to cause
  instability and system hangs for many users.

* Wed Feb 22 2006 Adam Jackson <ajackson@redhat.com> 6.4.2-4
- rebuilt

* Sun Feb 19 2006 Ray Strode <rstrode@redhat.com> 6.4.2-3
- enable texture-from-drawable patch
- add glut-devel dependency

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 6.4.2-2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Mike A. Harris <mharris@redhat.com> 6.4.2-2
- Added new "glx-utils" subpackage with glxgears and glxinfo (#173510)
- Added mesa-6.4.2-dprintf-to-debugprintf-for-bug180122.patch to workaround
  a Mesa namespace conflict with GNU_SOURCE (#180122)
- Added mesa-6.4.2-xorg-server-uses-bad-datatypes-breaking-AMD64-fdo5835.patch
  as an attempt to fix bugs (#176976,176414,fdo#5835)
- Enabled inclusion of the *EXPERIMENTAL UNSUPPORTED* r300 DRI driver on
  x86, x86_64, and ppc architectures, however the 2D Radeon driver will soon
  be modified to require the user to manually turn experimental DRI support
  on with Option "dri" in xorg.conf to test it out and report all X bugs that
  occur while using it directly to X.Org bugzilla.  (#179712)
- Use "libOSMesa.so.6.4.0604*" glob in file manifest, to avoid having to
  update it each upstream release.

* Sat Feb 04 2006 Mike A. Harris <mharris@redhat.com> 6.4.2-1
- Updated to Mesa 6.4.2
- Use "libGLU.so.1.3.0604*" glob in file manifest, to avoid having to update it
  each upstream release.

* Tue Jan 24 2006 Mike A. Harris <mharris@redhat.com> 6.4.1-5
- Added missing "BuildRequires: expat-devel" for bug (#178525)
- Temporarily disabled mesa-6.4.1-texture-from-drawable.patch, as it fails
  to compile on at least ia64, and possibly other architectures.

* Tue Jan 17 2006 Kristian Høgsberg <krh@redhat.com> 6.4.1-4
- Add mesa-6.4.1-texture-from-drawable.patch to implement protocol
  support for GLX_EXT_texture_from_drawable extension.

* Sat Dec 24 2005 Mike A. Harris <mharris@redhat.com> 6.4.1-3
- Manually copy libGLw headers that Mesa forgets to install, to fix (#173879).
- Added mesa-6.4.1-libGLw-enable-motif-support.patch to fix (#175251).
- Removed "Conflicts" lines from libGL package, as they are "Obsoletes" now.
- Do not rename swrast libGL .so version, as it is the OpenGL version.

* Tue Dec 20 2005 Mike A. Harris <mharris@redhat.com> 6.4.1-2
- Rebuild to ensure libGLU gets rebuilt with new gcc with C++ compiler fixes.
- Changed the 3 devel packages to use Obsoletes instead of Conflicts for the
  packages the files used to be present in, as this is more friendy for
  OS upgrades.
- Added "Requires: libX11-devel" to mesa-libGL-devel package (#173712)
- Added "Requires: libGL-devel" to mesa-libGLU-devel package (#175253)

* Sat Dec 17 2005 Mike A. Harris <mharris@redhat.com> 6.4.1-1
- Updated MesaLib tarball to version 6.4.1 from Mesa project for X11R7 RC4.
- Added pkgconfig dependency.
- Updated "BuildRequires: libdrm-devel >= 2.0-1"
- Added Obsoletes lines to all the subpackages to have cleaner upgrades.
- Added mesa-6.4.1-amd64-assyntax-fix.patch to work around a build problem on
  AMD64, which is fixed in the 6.4 branch of Mesa CVS.
- Conditionalize libOSMesa inclusion, and default to not including it for now.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com> 6.4-5.1
- rebuilt

* Sun Nov 20 2005 Jeremy Katz <katzj@redhat.com> 6.4-5
- fix directory used for loading dri modules (#173679)
- install dri drivers as executable so they get stripped (#173292)

* Thu Nov 03 2005 Mike A. Harris <mharris@redhat.com> 6.4-4
- Wrote redhat-mesa-source-filelist-generator to dynamically generate the
  files to be included in the mesa-source subpackage, to minimize future
  maintenance.
- Fixed detection and renaming of software mesa .so version.

* Wed Nov 02 2005 Mike A. Harris <mharris@redhat.com> 6.4-3
- Hack: autodetect if libGL was given .so.1.5* and rename it to 1.2 for
  consistency on all architectures, and to avoid upgrade problems if we
  ever disable DRI on an arch and then re-enable it later.

* Wed Nov 02 2005 Mike A. Harris <mharris@redhat.com> 6.4-2
- Added mesa-6.4-multilib-fix.patch to instrument and attempt to fix Mesa
  bin/installmesa script to work properly with multilib lib64 architectures.
- Set and export LIB_DIR and INCLUDE_DIR in spec file 'install' section,
  and invoke our modified bin/installmesa directly instead of using
  "make install".
- Remove "include/GL/uglglutshapes.h", as it uses the GLUT license, and seems
  like an extraneous file anyway.
- Conditionalize the file manifest to include libGL.so.1.2 on DRI enabled
  builds, but use libGL.so.1.5.060400 instead on DRI disabled builds, as
  this is how upstream builds the library, although it is not clear to me
  why this difference exists yet (which was not in Xorg 6.8.2 Mesa).

* Thu Oct 27 2005 Mike A. Harris <mharris@redhat.com> 6.4-1
- Updated to new upstream MesaLib-6.4
- Updated libGLU.so.1.3.060400 entry in file manifest
- Updated "BuildRequires: libdrm-devel >= 1.0.5" to pick up fixes for the
  unichrome driver.

* Tue Sep 13 2005 Mike A. Harris <mharris@redhat.com> 6.3.2-6
- Fix redhat-mesa-driver-install and spec file to work right on multilib
  systems.
  
* Mon Sep 05 2005 Mike A. Harris <mharris@redhat.com> 6.3.2-5
- Fix mesa-libGL-devel to depend on mesa-libGL instead of mesa-libGLU.
- Added virtual "Provides: libGL..." entries for each subpackage as relevant.

* Mon Sep 05 2005 Mike A. Harris <mharris@redhat.com> 6.3.2-4
- Added the mesa-source subpackage, which contains part of the Mesa source
  code needed by other packages such as the X server to build stuff.

* Mon Sep 05 2005 Mike A. Harris <mharris@redhat.com> 6.3.2-3
- Added Conflicts/Obsoletes lines to all of the subpackages to make upgrades
  from previous OS releases, and piecemeal upgrades work as nicely as
  possible.

* Mon Sep 05 2005 Mike A. Harris <mharris@redhat.com> 6.3.2-2
- Wrote redhat-mesa-target script to simplify mesa build target selection.
- Wrote redhat-mesa-driver-install to install the DRI drivers and simplify
  per-arch conditionalization, etc.

* Sun Sep 04 2005 Mike A. Harris <mharris@redhat.com> 6.3.2-1
- Initial build.
