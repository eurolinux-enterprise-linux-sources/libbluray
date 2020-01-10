%global snapshot 0
%global tarball_date 20111023
%global git_hash e037110f11e707e223b715f70920913afecfe297
%global git_short %(echo '%{git_hash}' | cut -c -13)
%global build_pdf_doc 0

Name:           libbluray
Version:        0.2.3
%if %{snapshot}
Release:        0.10.%{tarball_date}git%{git_short}%{?dist}
%else
Release:        3%{?dist}
%endif
Summary:        Library to access Blu-Ray disks for video playback 
Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://www.videolan.org/developers/libbluray.html
%if %{snapshot}
# Use the commands below to generate a tarball.
# git clone git://git.videolan.org/libbluray.git
# cd libbluray
# git archive --format=tar %{git_hash} --prefix=libbluray/ | bzip2 > ../libbluray-$( date +%Y%m%d )git%{git_short}.tar.bz2
Source0:        %{name}-%{tarball_date}git%{git_short}.tar.bz2
%else
Source0:        ftp://ftp.videolan.org/pub/videolan/%{name}/%{version}/%{name}-%{version}.tar.bz2
%endif
Patch0:         libbluray-0.2.2-no_doxygen_timestamp.patch
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%if %{snapshot}
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
%endif
BuildRequires:  libxml2-devel
BuildRequires:  doxygen
BuildRequires:  texlive-latex
BuildRequires:  graphviz


%description
This package is aiming to provide a full portable free open source bluray
library, which can be plugged into popular media players to allow full bluray
navigation and playback on Linux. It will eventually be compatible with all
current titles, and will be easily portable and embeddable in standard players
such as mplayer and vlc.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%if %{snapshot}
%setup -q -n %{name}
%else
%setup -q
%endif
%patch0 -p1 -b .no_timestamp


%build
%if %{snapshot}
autoreconf -vif
%endif
%configure --disable-static \
%if %{build_pdf_doc}
           --enable-doxygen-pdf \
%else
           --disable-doxygen-pdf \
%endif
           --disable-doxygen-ps \
           --enable-doxygen-html \
           --enable-examples \

make %{?_smp_mflags}
make doxygen-doc
# Remove uneeded script
rm -f doc/doxygen/html/installdox 


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Install test utilities
for i in clpi_dump index_dump mobj_dump mpls_dump sound_dump
do install -Dp -m 0755 src/examples/$i $RPM_BUILD_ROOT%{_bindir}/$i; done;
for i in bd_info bdsplice hdmv_test libbluray_test list_titles 
do install -Dp -m755 src/examples/.libs/$i %{buildroot}%{_bindir}/$i; done

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING player_wrappers README.txt
%{_libdir}/*.so.*
%{_bindir}/*


%files devel
%defattr(-,root,root,-)
%doc doc/doxygen/html
%if %{build_pdf_doc}
%doc doc/doxygen/libbluray.pdf
%endif
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libbluray.pc


%changelog
* Fri May 03 2013 Bastien Nocera <bnocera@redhat.com> 0.2.3-3
- Remove unused java sub-package

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 21 2012 Xavier Bachelot <xavier@bachelot.org> 0.2.3-1
- Update to 0.2.3.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Xavier Bachelot <xavier@bachelot.org> 0.2.2-3
- Don't build pdf doc, it breaks multilib (see RHBZ#835952).

* Tue Jun 12 2012 Xavier Bachelot <xavier@bachelot.org> 0.2.2-2
- Fix multilib conflict in doxygen docs (RHBZ#831401).

* Tue Mar 20 2012 Xavier Bachelot <xavier@bachelot.org> 0.2.2-1
- Update to 0.2.2.

* Tue Mar 20 2012 Karsten Hopp <karsten@redhat.com> 0.2.1-4
- ppc(64) has no java-1.7.0-open yet, disable java subpackage on both PPC archs

* Thu Mar 15 2012 Rex Dieter <rdieter@fedoraproject.org> 0.2.1-3
- make build non-fatal when using doxygen-1.8 (doesn't produce installdox anymore)

* Wed Feb 01 2012 Xavier Bachelot <xavier@bachelot.org> 0.2.1-2
- Rebuild for openjdk 7.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 01 2011 Xavier Bachelot <xavier@bachelot.org> 0.2.1-1
- First upstream official release.
- Fix BD-J build (missing files in upstream tarball).
- Have subpackages require an arch-specific base package.

* Sun Oct 23 2011 Xavier Bachelot <xavier@bachelot.org> 0.2-0.7.20111023gite037110f11e70
- Update to latest snapshot.

* Sat Jul 16 2011 Xavier Bachelot <xavier@bachelot.org> 0.2-0.6.20110710git51d7d60a96d06
- Don't build java subpackage on ppc64, no java-1.6.0-devel package.

* Sun Jul 10 2011 Xavier Bachelot <xavier@bachelot.org> 0.2-0.5.20110710git51d7d60a96d06
- Update to latest snapshot.

* Sat May 14 2011 Xavier Bachelot <xavier@bachelot.org> 0.2-0.4.20110514git46ee2766038e9
- Update to latest snapshot.
- Drop -static subpackage.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-0.3.20110126gitbbf11e43bd82e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Xavier Bachelot <xavier@bachelot.org> 0.2-0.2.20110126gitbbf11e43bd82e
- Update to latest snapshot.
- Split the BDJ support to a -java subpackage.

* Fri Jan 07 2011 Xavier Bachelot <xavier@bachelot.org> 0.2-0.1.20110107git0e5902ff9a6f1
- Update to latest snapshot.
- Add BR: libxml2-devel for metadata parser.
- Add BR: graphviz for doc generation.

* Thu Oct 28 2010 Xavier Bachelot <xavier@bachelot.org> 0.1-0.3.20101028gitc32862b77dea4
- Update to latest snapshot.
- Install BDJ jar.

* Thu Oct 21 2010 Xavier Bachelot <xavier@bachelot.org> 0.1-0.2.20101021git144a204c02687
- Fix release tag.
- Update to latest snapshot.

* Thu Aug 19 2010 Xavier Bachelot <xavier@bachelot.org> 0.1-0.1.20100819
- Initial Fedora release.
