%define realname boto
Summary:	An integrated interface to infrastructural services offered by Amazon Web Services
Summary(pl.UTF-8):	Zintegrowany interfejs do usług infrastruktury oferowanych przez usługi WWW Amazon
Name:		python-%{realname}
Version:	2.0
%define 	beta	b4
Release:	0.%{beta}.1
License:	MIT
Group:		Libraries/Python
Source0:	http://boto.googlecode.com/files/%{realname}-%{version}%{beta}.tar.gz
# Source0-md5:	f00ccf9167fee01d6a415bd4ab156171
URL:		http://code.google.com/p/boto/
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%pyrequires_eq	python-libs
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An integrated interface to current and future infrastructural services
offered by Amazon Web Services.

%description -l pl.UTF-8
Zintegrowany interfejs do aktualnych i przyszłych usług infrastruktury
oferowanych przez usługi WWW Amazon.

%package -n boto
Summary:	Python utilities for Amazon Web Services
Group:		Applications
Requires:	%{name} = %{version}-%{release}

%description -n boto
Boto is an integrated Python interface to current and future infrastructural
services offered by Amazon Web Services. 

This package includes sample utilities implemented with this API.

%prep
%setup -q -n %{realname}-%{version}%{beta}

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--root=$RPM_BUILD_ROOT \
	--optimize=2
rm -rf $RPM_BUILD_ROOT%{py_sitescriptdir}/tests

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc PKG-INFO README 
%{py_sitescriptdir}/boto
%{py_sitescriptdir}/boto-*.egg-info

%files -n boto
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
