%define realname boto
Summary:	An integrated interface to infrastructural services offered by Amazon Web Services
Summary(pl.UTF-8):	Zintegrowany interfejs do usług infrastruktury oferowanych przez usługi WWW Amazon
Name:		python-%{realname}
Version:	1.2a
Release:	2
License:	MIT
Group:		Libraries/Python
Source0:	http://boto.googlecode.com/files/%{realname}-%{version}.tar.gz
# Source0-md5:	e4329f02ad17837b6e4b1269e1ae63e3
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

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{py_sitescriptdir}/boto
