%define realname boto
Summary:	An integrated interface to infrastructural services offered by Amazon Web Services
Summary(pl.UTF-8):	Zintegrowany interfejs do usług infrastruktury oferowanych przez usługi WWW Amazon
Name:		python-%{realname}
Version:	1.9b
Release:	1
License:	MIT
Group:		Libraries/Python
Source0:	http://boto.googlecode.com/files/%{realname}-%{version}.tar.gz
# Source0-md5:	4fc2fd7b70a971b1363f8465aafe7091
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

#install -d $RPM_BUILD_ROOT%{_bindir}
#install cq.py s3put $RPM_BUILD_ROOT%{_bindir}

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc PKG-INFO README 
%attr(755,root,root) %{_bindir}/elbadmin
%attr(755,root,root) %{_bindir}/fetch_file
%attr(755,root,root) %{_bindir}/launch_instance
%attr(755,root,root) %{_bindir}/list_instances
%attr(755,root,root) %{_bindir}/s3put
%attr(755,root,root) %{_bindir}/sdbadmin
%attr(755,root,root) %{_bindir}/taskadmin
%{py_sitescriptdir}/boto
%{py_sitescriptdir}/boto-*.egg-info
