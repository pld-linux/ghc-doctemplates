#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	doctemplates
Summary:	Pandoc-style document templates
Name:		ghc-%{pkgname}
Version:	0.8.2
Release:	2
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/doctemplates
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	84be788ba38ad7983076fe698260e028
URL:		http://hackage.haskell.org/package/doctemplates
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-aeson
BuildRequires:	ghc-doclayout
BuildRequires:	ghc-HsYAML
BuildRequires:	ghc-scientific
BuildRequires:	ghc-semigroups
BuildRequires:	ghc-text-conversions
BuildRequires:	ghc-unordered-containers
BuildRequires:	ghc-vector
%if %{with prof}
BuildRequires:	ghc-prof
BuildRequires:	ghc-aeson-prof
BuildRequires:	ghc-doclayout-prof
BuildRequires:	ghc-HsYAML-prof
BuildRequires:	ghc-scientific-prof
BuildRequires:	ghc-semigroups-prof
BuildRequires:	ghc-text-conversions-prof
BuildRequires:	ghc-unordered-containers-prof
BuildRequires:	ghc-vector-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires:	ghc-aeson
Requires:	ghc-doclayout
Requires:	ghc-HsYAML
Requires:	ghc-scientific
Requires:	ghc-semigroups
Requires:	ghc-text-conversions
Requires:	ghc-unordered-containers
Requires:	ghc-vector
Requires(post,postun):	/usr/bin/ghc-pkg
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
This is the text templating system used by pandoc. It supports
variable interpolation, iteration, tests for non-blank values, pipes,
and partials. Templates are rendered to doclayout Docs, and variable
values may come from a variety of different sources, including aeson
Values.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-prof
Requires:	ghc-aeson-prof
Requires:	ghc-doclayout-prof
Requires:	ghc-HsYAML-prof
Requires:	ghc-scientific-prof
Requires:	ghc-semigroups-prof
Requires:	ghc-text-conversions-prof
Requires:	ghc-unordered-containers-prof
Requires:	ghc-vector-prof

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc README.md changelog.md %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/DocTemplates
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/DocTemplates/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/DocTemplates/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/DocTemplates/*.p_hi
%endif
