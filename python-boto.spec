%define realname boto
Summary:	An integrated interface to infrastructural services offered by Amazon Web Services
Summary(pl.UTF-8):	Zintegrowany interfejs do usług infrastruktury oferowanych przez usługi WWW Amazon
Name:		python-%{realname}
Version:	1.6b
Release:	1
License:	MIT
Group:		Libraries/Python
Source0:	http://boto.googlecode.com/files/%{realname}-%{version}.tar.gz
# Source0-md5:	da35ce449ed0be74a3e5d9fff58f9d08
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

%prep
%setup -q -n %{realname}-%{version}

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--root=$RPM_BUILD_ROOT \
	--optimize=2
rm -rf $RPM_BUILD_ROOT%{py_sitescriptdir}/tests

install -d $RPM_BUILD_ROOT%{_bindir}
install cq.py s3put $RPM_BUILD_ROOT%{_bindir}

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc PKG-INFO README doc/*
%attr(755,root,root) %{_bindir}/cq.py
%attr(755,root,root) %{_bindir}/s3put
%{py_sitescriptdir}/boto
