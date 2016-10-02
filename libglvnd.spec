%global commit 14f6283
%global vermagic 0.2.999
%global snapshot .git20161002.%{commit}

%global __provides_exclude ^(libGL[.]so|libOpenGL[.]so|libEGL[.]so|libGLESv1_CM[.]so|libGLESv2[.]so|libGLX[.]so).*$
%global __requires_exclude ^(libGL[.]so|libOpenGL[.]so|libEGL[.]so|libGLESv1_CM[.]so|libGLESv2[.]so|libGLX[.]so).*$

Name:           libglvnd
Version:        %{vermagic}
Release:        1%{snapshot}%{?dist}
Summary:        The GL Vendor-Neutral Dispatch library

License:        BSD
URL:            https://github.com/NVIDIA/libglvnd

# git clone https://github.com/NVIDIA/libglvnd
# cd libglvnd
# ./autogen.sh && ./configure && make dist
Source0:        libglvnd-%{version}.tar.gz
Source1:        LICENSE.libglvnd
Source2:        glvnd-x86_64.conf
Patch0:         libglvnd-fix-addr-may-be-used-unintialized.patch

BuildRequires:  python
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(glproto)

%description
This is a work-in-progress implementation of the vendor-neutral dispatch layer
for arbitrating OpenGL API calls between multiple vendors on a per-screen basis


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        -n glvnd-libGL
Summary:        GLVND libGL runtime library
Requires:       glvnd-libGLX%{?_isa} = %{version}-%{release}

%description    -n glvnd-libGL
%{Summary}.


%package        -n glvnd-libOpenGL
Summary:        GLVND libOpenGL runtime library

%description    -n glvnd-libOpenGL
%{Summary}.


%package        -n glvnd-libEGL
Summary:        GLVND libEGL runtime library

%description    -n glvnd-libEGL
%{Summary}.


%package        -n glvnd-libGLES
Summary:        GLVND libGLES runtime library

%description    -n glvnd-libGLES
%{Summary}.


%package        -n glvnd-libGLX
Summary:        GLVND libGLX runtime library

%description    -n glvnd-libGLX
%{Summary}.


%prep
%setup -q
%patch0 -p1

# license text extracted from README.md
cp %{SOURCE1} .


%build
%configure \
    --libdir=%{_libdir}/glvnd \
    --disable-static \
    --disable-silent-rules
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'

# ld.so search path
install -D -p -m644 %{SOURCE2} %{buildroot}/etc/ld.so.conf.d/glvnd-x86_64.conf

# Is everything ok with the upstream pc-file from the beginning?
mv %{buildroot}%{_libdir}/glvnd/pkgconfig %{buildroot}%{_libdir}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post -n glvnd-libGL -p /sbin/ldconfig
%postun -n glvnd-libGL -p /sbin/ldconfig

%post -n glvnd-libOpenGL -p /sbin/ldconfig
%postun -n glvnd-libOpenGL -p /sbin/ldconfig

%post -n glvnd-libEGL -p /sbin/ldconfig
%postun -n glvnd-libEGL -p /sbin/ldconfig

%post -n glvnd-libGLES -p /sbin/ldconfig
%postun -n glvnd-libGLES -p /sbin/ldconfig

%post -n glvnd-libGLX -p /sbin/ldconfig
%postun -n glvnd-libGLX -p /sbin/ldconfig


%files
%doc README.md
%license LICENSE.libglvnd
/etc/ld.so.conf.d/*.conf
%{_libdir}/glvnd/libGLdispatch.so.*

%files -n glvnd-libGL
%{_libdir}/glvnd/libGL.so.*

%files -n glvnd-libOpenGL
%{_libdir}/glvnd/libOpenGL.so.*

%files -n glvnd-libEGL
%{_libdir}/glvnd/libEGL.so.*

%files -n glvnd-libGLES
%{_libdir}/glvnd/libGLESv*.so.*

%files -n glvnd-libGLX
%{_libdir}/glvnd/libGLX.so.*

%files devel
%{_includedir}/*
%{_libdir}/glvnd/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Sun Oct 02 2016 Jajauma's Packages <jajauma@yandex.ru> - 0.2.999-1.git20161002.14f6283}
- Public release
