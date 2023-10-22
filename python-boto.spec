#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define module boto
Summary:	An integrated interface to infrastructural services offered by Amazon Web Services
Summary(pl.UTF-8):	Zintegrowany interfejs do usług infrastruktury oferowanych przez usługi WWW Amazon
Name:		python-%{module}
Version:	2.49.0
Release:	6
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/boto/
Source0:	https://files.pythonhosted.org/packages/source/b/boto/boto-%{version}.tar.gz
# Source0-md5:	e9b79f80198da059d9a8055a5352fd6d
Patch0:		%{name}-mock.patch
Patch1:		%{name}-py3.patch
# https://github.com/boto/boto/pull/3086 (unbundle six)
Patch2:		boto-devendor.patch
# https://github.com/boto/boto/pull/3472
Patch3:		boto-nat-gateway.patch
# https://github.com/boto/boto/pull/3506
# https://github.com/boto/boto/pull/3508
Patch4:		boto-retry-float.patch
# https://github.com/boto/boto/pull/3332
Patch5:		boto-aws-exec-read.patch
# https://github.com/boto/boto/pull/3077
# https://github.com/boto/boto/pull/3131
Patch6:		boto-instance-attributes.patch
# https://github.com/boto/boto/pull/2882
Patch7:		boto-multi-vpc-zone.patch
# https://github.com/boto/boto/pull/2875
Patch8:		boto-s3-requestlog.patch
# https://github.com/boto/boto/pull/2866
Patch9:		boto-route53-no-resourcepath.patch
# https://github.com/boto/boto/pull/3111
Patch10:	boto-modifysubnetattribute.patch
URL:		https://github.com/boto/boto
%if %{with python2}
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-httpretty
BuildRequires:	python-mock
BuildRequires:	python-nose
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.3
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-httpretty
BuildRequires:	python3-nose
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-2
%endif
Requires:	python-modules >= 1:2.6
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
Requires:	python3-modules >= 1:3.3

%description -n python3-%{module}
An integrated interface to current and future infrastructural services
offered by Amazon Web Services.

%description -n python3-%{module} -l pl.UTF-8
Zintegrowany interfejs do aktualnych i przyszłych usług infrastruktury
oferowanych przez usługi WWW Amazon.

%package -n boto
Summary:	Python utilities for Amazon Web Services
Summary(pl.UTF-8):	Pythonowe narzędzia do usług AWS
Group:		Applications/Networking
%if %{with python3}
Requires:	python3-%{module} = %{version}-%{release}
%else
Requires:	%{name} = %{version}-%{release}
%endif

%description -n boto
Boto is an integrated Python interface to current and future
infrastructural services offered by Amazon Web Services.

This package includes sample utilities implemented with this API.

%description -n boto -l pl.UTF-8
Boto to zintegrowany interfejs do aktualnych i przyszłych usług
infrastruktury oferowanych przez usługi AWS (Amazon WWW Services).

Ten pakiet zawiera przykładowe narzędzia zaimplementowane przy użyciu
API boto.

%package apidocs
Summary:	API documentation for Python boto module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona boto
Group:		Documentation

%description apidocs
API documentation for Python boto module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona boto.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
nosetests-%{py_ver} tests/unit -a '!notdefault'
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
nosetests-%{py3_ver} tests/unit -a '!notdefault'
%endif
%endif

%if %{with doc}
# docs are not ready for python3
PYTHONPATH=$(pwd) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

for bin in asadmin bundle_image cfadmin cq cwutil dynamodb_dump dynamodb_load elbadmin \
	   fetch_file glacier instance_events kill_instance launch_instance list_instances \
	   lss3 mturk pyami_sendmail route53 s3put sdbadmin taskadmin ; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/${bin} $RPM_BUILD_ROOT%{_bindir}/${bin}-2
%if %{without python3}
	ln -sf ${bin}-2 $RPM_BUILD_ROOT%{_bindir}/${bin}
%endif
done

%py_postclean
%endif

%if %{with python3}
%py3_install

for bin in asadmin bundle_image cfadmin cq cwutil dynamodb_dump dynamodb_load elbadmin \
	   fetch_file glacier instance_events kill_instance launch_instance list_instances \
	   lss3 mturk pyami_sendmail route53 s3put sdbadmin taskadmin ; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/${bin} $RPM_BUILD_ROOT%{_bindir}/${bin}-3
	ln -sf ${bin}-3 $RPM_BUILD_ROOT%{_bindir}/${bin}
done
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst
%attr(755,root,root) %{_bindir}/asadmin-2
%attr(755,root,root) %{_bindir}/bundle_image-2
%attr(755,root,root) %{_bindir}/cfadmin-2
%attr(755,root,root) %{_bindir}/cq-2
%attr(755,root,root) %{_bindir}/cwutil-2
%attr(755,root,root) %{_bindir}/dynamodb_dump-2
%attr(755,root,root) %{_bindir}/dynamodb_load-2
%attr(755,root,root) %{_bindir}/elbadmin-2
%attr(755,root,root) %{_bindir}/fetch_file-2
%attr(755,root,root) %{_bindir}/glacier-2
%attr(755,root,root) %{_bindir}/instance_events-2
%attr(755,root,root) %{_bindir}/kill_instance-2
%attr(755,root,root) %{_bindir}/launch_instance-2
%attr(755,root,root) %{_bindir}/list_instances-2
%attr(755,root,root) %{_bindir}/lss3-2
%attr(755,root,root) %{_bindir}/mturk-2
%attr(755,root,root) %{_bindir}/pyami_sendmail-2
%attr(755,root,root) %{_bindir}/route53-2
%attr(755,root,root) %{_bindir}/s3put-2
%attr(755,root,root) %{_bindir}/sdbadmin-2
%attr(755,root,root) %{_bindir}/taskadmin-2
%{py_sitescriptdir}/boto
%{py_sitescriptdir}/boto-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README.rst
%attr(755,root,root) %{_bindir}/asadmin-3
%attr(755,root,root) %{_bindir}/bundle_image-3
%attr(755,root,root) %{_bindir}/cfadmin-3
%attr(755,root,root) %{_bindir}/cq-3
%attr(755,root,root) %{_bindir}/cwutil-3
%attr(755,root,root) %{_bindir}/dynamodb_dump-3
%attr(755,root,root) %{_bindir}/dynamodb_load-3
%attr(755,root,root) %{_bindir}/elbadmin-3
%attr(755,root,root) %{_bindir}/fetch_file-3
%attr(755,root,root) %{_bindir}/glacier-3
%attr(755,root,root) %{_bindir}/instance_events-3
%attr(755,root,root) %{_bindir}/kill_instance-3
%attr(755,root,root) %{_bindir}/launch_instance-3
%attr(755,root,root) %{_bindir}/list_instances-3
%attr(755,root,root) %{_bindir}/lss3-3
%attr(755,root,root) %{_bindir}/mturk-3
%attr(755,root,root) %{_bindir}/pyami_sendmail-3
%attr(755,root,root) %{_bindir}/route53-3
%attr(755,root,root) %{_bindir}/s3put-3
%attr(755,root,root) %{_bindir}/sdbadmin-3
%attr(755,root,root) %{_bindir}/taskadmin-3
%{py3_sitescriptdir}/boto
%{py3_sitescriptdir}/boto-%{version}-py*.egg-info
%endif

%files -n boto
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/asadmin
%attr(755,root,root) %{_bindir}/bundle_image
%attr(755,root,root) %{_bindir}/cfadmin
%attr(755,root,root) %{_bindir}/cq
%attr(755,root,root) %{_bindir}/cwutil
%attr(755,root,root) %{_bindir}/dynamodb_dump
%attr(755,root,root) %{_bindir}/dynamodb_load
%attr(755,root,root) %{_bindir}/elbadmin
%attr(755,root,root) %{_bindir}/fetch_file
%attr(755,root,root) %{_bindir}/glacier
%attr(755,root,root) %{_bindir}/instance_events
%attr(755,root,root) %{_bindir}/kill_instance
%attr(755,root,root) %{_bindir}/launch_instance
%attr(755,root,root) %{_bindir}/list_instances
%attr(755,root,root) %{_bindir}/lss3
%attr(755,root,root) %{_bindir}/mturk
%attr(755,root,root) %{_bindir}/pyami_sendmail
%attr(755,root,root) %{_bindir}/route53
%attr(755,root,root) %{_bindir}/s3put
%attr(755,root,root) %{_bindir}/sdbadmin
%attr(755,root,root) %{_bindir}/taskadmin

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,migrations,ref,releasenotes,*.html,*.js}
%endif
