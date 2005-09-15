#!/bin/bash
# NOTE: /bin/bash shebang on first line to get shell script syntax
# highlighting in mcedit.  (temporary hack)

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

Summary: Mesa graphics libraries
Name: mesa
Version: 6.3.2
Release: 7
License: MIT/X11
Group: System Environment/Libraries
URL: http://www.mesa3d.org
Source0: MesaLib-%{version}.tar.bz2
# FIXME; Upstream Mesa 6.3.2 as shipped is broken and missing files for
# the linux-dri-x86 target.
Source1: redhat-mesa-target
Source2: redhat-mesa-driver-install
Source5: mesa-source-filelist.in
Source10: r200_vtxtmp_x86.S
Source11: radeon_vtxtmp_x86.S
#Patch0: mesa-6.3.2-makedepend.patch
Patch0: mesa-6.3.2-build-configuration-v4.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires: libdrm-devel
BuildRequires: libXxf86vm-devel

%description
Mesa

#-- libGL ------------------------------------------------------------
%package libGL
Summary: Mesa libGL runtime libraries and DRI drivers.
Group: System Environment/Libraries

Provides: libGL

# libGL used to be in Mesa package in RHL 6.x, 7.[0-2], RHEL 2.1
Conflicts: Mesa
Obsoletes: Mesa
# libGL moved to XFree86-libs for RHL 7.3
Conflicts: XFree86-libs
# libGL moved to XFree86-Mesa-libGL for RHL 8.0, 9, FC1, RHEL 3
Conflicts: XFree86-Mesa-libGL
Obsoletes: XFree86-Mesa-libGL
# libGL moved to xorg-x11-Mesa-libGL for FC[2-4], RHEL4
Conflicts: xorg-x11-Mesa-libGL
Obsoletes: xorg-x11-Mesa-libGL
# Conflict with the xorg-x11-libs too, just to be safe for file conflicts
Conflicts: xorg-x11-libs

%description libGL
Mesa libGL runtime libraries and DRI drivers.
#-- libGLw -----------------------------------------------------------
%package libGL-devel
Summary: Mesa libGL development package
Group: Development/Libraries
Requires: libGL = %{version}-%{release}

Provides: libGL-devel

# libGL devel files were in Mesa-devel package in RHL 6.x, 7.[0-2], RHEL 2.1
Conflicts: Mesa-devel
Obsoletes: Mesa-devel
# libGL devel files moved to XFree86-devel for RHL 7.3, 8.0, 9, FC1, RHEL 3
Conflicts: XFree86-devel
# libGL devel files moved to xorg-x11-devel for FC2, FC3, FC4
Conflicts: xorg-x11-devel

%description libGL-devel
Mesa libGL development package
#-- libGLw -----------------------------------------------------------
%package libGLU
Summary: Mesa libGLU runtime library
Group: System Environment/Libraries

Provides: libGLU

# libGLU used to be in Mesa package in RHL 6.x, 7.[0-2], RHEL 2.1
Conflicts: Mesa
Obsoletes: Mesa
# libGLU moved to XFree86-libs for RHL 7.3
Conflicts: XFree86-libs
# libGLU moved to XFree86-Mesa-libGLU for RHL 8.0, 9, FC1, RHEL 3
Conflicts: XFree86-Mesa-libGLU
Obsoletes: XFree86-Mesa-libGLU
# libGLU moved to xorg-x11-Mesa-libGLU for FC[2-4], RHEL4
Conflicts: xorg-x11-Mesa-libGLU
Obsoletes: xorg-x11-Mesa-libGLU
# Conflict with the xorg-x11-libs too, just to be safe for file conflicts
Conflicts: xorg-x11-libs

%description libGLU
Mesa libGLU runtime library
#-- libGLw -----------------------------------------------------------
%package libGLU-devel
Summary: Mesa libGLU development package
Group: Development/Libraries
Requires: libGLU = %{version}-%{release}

Provides: libGLU-devel

# libGLU devel files were in Mesa-devel package in RHL 6.x, 7.[0-2], RHEL 2.1
Conflicts: Mesa-devel
Obsoletes: Mesa-devel
# libGLU devel files moved to XFree86-devel for RHL 7.3, 8.0, 9, FC1, RHEL 3
Conflicts: XFree86-devel
# libGLU devel files moved to xorg-x11-devel for FC2, FC3, FC4
Conflicts: xorg-x11-devel

%description libGLU-devel
Mesa libGLU development package
#-- libGLw -----------------------------------------------------------
%package libGLw
Summary: Mesa libGLw runtime library
Group: System Environment/Libraries

Provides: libGLw

# libGLw used to be in Mesa package in RHL 6.x, 7.[0-2], RHEL 2.1
Conflicts: Mesa
Obsoletes: Mesa
# libGLw moved to XFree86-libs for RHL 7.3, 8, 9, FC1, RHEL 3
Conflicts: XFree86-libs
# libGLw moved to xorg-x11-libs FC[2-4], RHEL4
Conflicts: xorg-x11-libs

%description libGLw
Mesa libGLw runtime library
#-- libGLw-devel -----------------------------------------------------
%package libGLw-devel
Summary: Mesa libGLw development package
Group: Development/Libraries
Requires: libGLw = %{version}-%{release}

Provides: libGLw-devel

# libGLw devel files were in Mesa-devel package in RHL 6.x, 7.[0-2], RHEL 2.1
Conflicts: Mesa-devel
Obsoletes: Mesa-devel
# libGLw devel files moved to XFree86-devel for RHL 7.3, 8.0, 9, FC1, RHEL 3
Conflicts: XFree86-devel
# libGLw devel files moved to xorg-x11-devel for FC2, FC3, FC4
Conflicts: xorg-x11-devel

%description libGLw-devel
Mesa libGLw development package
#-- source -----------------------------------------------------------
%package source
Summary: Mesa source code required to build X server
Group: Development/Libraries

%description source
The mesa-source package provides the minimal source code needed to
build DRI enabled X servers, etc.


#-- Prep -------------------------------------------------------------
%prep
%setup -q -n Mesa-%{version}
# Copy Red Hat Mesa build/install simplification scripts into build dir.
install -m 755 %{SOURCE1} ./
install -m 755 %{SOURCE2} ./
# FIXME: Install files missing from upstream Mesa 6.3.2 source
cp %{SOURCE10} src/mesa/drivers/dri/r200/
cp %{SOURCE11} src/mesa/drivers/dri/radeon/

#%patch0 -p0 -b .makedepend


#-- Build ------------------------------------------------------------
%build
# Macroize this to simplify things
%define makeopts MKDEP="gcc -M" MKDEP_OPTIONS="-MF depend"
# NOTE: We use a custom script to determine which Mesa build target should
# be used, and reduce spec file clutter.
MESATARGET="$(./redhat-mesa-target %{with_dri} %{_arch})"
make ${MESATARGET} %{makeopts}


#-- Install ----------------------------------------------------------
%install
rm -rf $RPM_BUILD_ROOT
#%%makeinstall DESTDIR=$RPM_BUILD_ROOT

# The mesa make install target use a small shell script that doesn't
# know about multilib systems.  The crux of the shell script is
# basically these 5 lines, so we just do it here.

mkdir -p $RPM_BUILD_ROOT%{_includedir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}/GL
mkdir -p $RPM_BUILD_ROOT%{_libdir}
cp -f include/GL/*.h $RPM_BUILD_ROOT%{_includedir}/GL
cp -fd %{_lib}/lib* $RPM_BUILD_ROOT%{_libdir}

%if %{with_dri}
export DRIMODULE_SRCDIR="%{_lib}"
export DRIMODULE_DESTDIR="$RPM_BUILD_ROOT%{_libdir}/dri"
echo "DRIMODULE_SRCDIR=$DRIMODULE_SRCDIR"
echo "DRIMODULE_DESTDIR=$DRIMODULE_DESTDIR"
./redhat-mesa-driver-install %{_arch}
%endif

# Install source code files for mesa-source subpackage
{
%define mesa_source_filelist mesa-source-files.lst
%define mesasourcedir %{_datadir}/mesa/source

    touch %{mesa_source_filelist}
    for file in $(sort < %{SOURCE5} | uniq) ; do
        DSTDIR=$RPM_BUILD_ROOT%{mesasourcedir}/${file%/*}
        [ ! -d $DSTDIR ] && mkdir -p $DSTDIR
        install -m 444 $file $DSTDIR/
        # Write file to rpm file list manifest
        echo "%%{mesasourcedir}/${file}" >> %{mesa_source_filelist}
    done
    # Search mesa source dir for directories the package should own
    find $RPM_BUILD_ROOT%{mesasourcedir} -type d | \
         sed -e "s#^$RPM_BUILD_ROOT%{mesasourcedir}#%dir %%{mesasourcedir}#g" >> %{mesa_source_filelist}
    # Ugly hack to cause the 'mesa' dir to be owned by the package too.
    echo "%dir %%{_datadir}/mesa" >> %{mesa_source_filelist}
}

# No glut stuff.
rm $RPM_BUILD_ROOT%{_includedir}/GL/uglglutshapes.h
#rm $RPM_BUILD_ROOT%{_includedir}/GL/uglmesa.h


#-- Clean ------------------------------------------------------------
%clean
rm -rf $RPM_BUILD_ROOT

#-- Check ------------------------------------------------------------
%check

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
# x86 DRI modules
%if %{with_dri}
%dir %{_libdir}/dri
# NOTE: This is a glob for now, as we explicitly determine and limit the DRI
# drivers that are installed on a given OS/arch combo in our custom DRI
# driver install script.  If the upstream install script improves enough to
# make our script unnecessary, we might want to change to an explicit file
# manifest here in the future.
%{_libdir}/dri/*_dri.so
# NOTE: Documentive list of all DRI drivers built by default in Mesa 6.3.2
#%{_libdir}/dri/ffb_dri.so
#%{_libdir}/dri/i810_dri.so
#%{_libdir}/dri/i830_dri.so
#%{_libdir}/dri/i915_dri.so
#%{_libdir}/dri/mach64_dri.so
#%{_libdir}/dri/mga_dri.so
#%{_libdir}/dri/r128_dri.so
#%{_libdir}/dri/r200_dri.so
#%{_libdir}/dri/r300_dri.so
#%{_libdir}/dri/radeon_dri.so
#%{_libdir}/dri/s3v_dri.so
#%{_libdir}/dri/savage_dri.so
#%{_libdir}/dri/sis_dri.so
#%{_libdir}/dri/tdfx_dri.so
#%{_libdir}/dri/trident_dri.so
#%{_libdir}/dri/unichrome_dri.so
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

%files source -f %{mesa_source_filelist}
%defattr(-,root,root,-)

%changelog
* Thu Sep 15 2005 Kristian Høgsberg <krh@redhat.com> 6.3.2-7
- Copy files manually instead of using the mesa install script.

* Tue Sep 13 2005 Mike A. Harris <mharris@redhat.com> 6.3.2-6
- Fix redhat-mesa-driver-install and spec file to work right on multilib
  systems.
  
* Mon Sep 5 2005 Mike A. Harris <mharris@redhat.com> 6.3.2-5
- Fix mesa-libGL-devel to depend on mesa-libGL instead of mesa-libGLU.
- Added virtual "Provides: libGL..." entries for each subpackage as relevant.

* Mon Sep 5 2005 Mike A. Harris <mharris@redhat.com> 6.3.2-4
- Added the mesa-source subpackage, which contains part of the Mesa source
  code needed by other packages such as the X server to build stuff.

* Mon Sep 5 2005 Mike A. Harris <mharris@redhat.com> 6.3.2-3
- Added Conflicts/Obsoletes lines to all of the subpackages to make upgrades
  from previous OS releases, and piecemeal upgrades work as nicely as
  possible.

* Mon Sep 5 2005 Mike A. Harris <mharris@redhat.com> 6.3.2-2
- Wrote redhat-mesa-target script to simplify mesa build target selection.
- Wrote redhat-mesa-driver-install to install the DRI drivers and simplify
  per-arch conditionalization, etc.

* Sun Sep 4 2005 Mike A. Harris <mharris@redhat.com> 6.3.2-1
- Initial build.
