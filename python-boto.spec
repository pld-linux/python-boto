%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define module boto
Summary:	An integrated interface to infrastructural services offered by Amazon Web Services
Summary(pl.UTF-8):	Zintegrowany interfejs do usług infrastruktury oferowanych przez usługi WWW Amazon
Name:		python-%{module}
Version:	2.42.0
Release:	2
License:	MIT
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/c4/bb/28324652bedb4ea9ca77253b84567d1347b54df6231b51822eaaa296e6e0/boto-%{version}.tar.gz
# Source0-md5:	62b6ef1af3d18f8811f97e311b856dad
URL:		https://github.com/boto/boto
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
Requires:	python-libs
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An integrated interface to current and future infrastructural services
offered by Amazon Web Services.

%description -l pl.UTF-8
Zintegrowany interfejs do aktualnych i przyszłych usług infrastruktury
oferowanych przez usługi WWW Amazon.

%package -n python3-%{module}
Summary:	An integrated interface to infrastructural services offered by Amazon Web Services
Summary(pl.UTF-8):	Zintegrowany interfejs do usług infrastruktury oferowanych przez usługi WWW Amazon
Group:		Libraries/Python

%description -n python3-%{module}
An integrated interface to current and future infrastructural services
offered by Amazon Web Services.

%description -n python3-%{module} -l pl.UTF-8
Zintegrowany interfejs do aktualnych i przyszłych usług infrastruktury
oferowanych przez usługi WWW Amazon.

%package -n boto
Summary:	Python utilities for Amazon Web Services
Group:		Applications
Requires:	%{name} = %{version}-%{release}

%description -n boto
Boto is an integrated Python interface to current and future
infrastructural services offered by Amazon Web Services.

This package includes sample utilities implemented with this API.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with python2}
%py_build %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python3}
%py3_install
rm -rf $RPM_BUILD_ROOT%{py3_sitescriptdir}/tests
%endif

%if %{with python2}
rm -rf $RPM_BUILD_ROOT%{_bindir}
%py_install

rm -rf $RPM_BUILD_ROOT%{py_sitescriptdir}/tests
%py_postclean
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc PKG-INFO README*
%{py_sitescriptdir}/boto
%{py_sitescriptdir}/boto-*.egg-info

%files -n python3-%{module}
%defattr(644,root,root,755)
%doc PKG-INFO README*
%{py3_sitescriptdir}/boto
%{py3_sitescriptdir}/boto-*.egg-info

%files -n boto
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
