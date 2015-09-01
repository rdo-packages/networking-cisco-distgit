%global drv_vendor Cisco
%global srcname networking_cisco
%global package_name networking-cisco
%global docpath doc/build/html

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-%{package_name}
Version:        XXX
Release:        XXX
Summary:        %{drv_vendor} OpenStack Neutron driver

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/%{package_name}
Source0:        https://pypi.python.org/packages/source/n/networking-cisco/networking-cisco-2015.1.2.tar.gz
Source1:        neutron-cisco-cfg-agent.service

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-mock
BuildRequires:  python-neutron-tests
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx
BuildRequires:  python-testrepository
BuildRequires:  python-testtools
BuildRequires:	systemd-units

Requires:       python-babel
Requires:       python-pbr
Requires:       openstack-neutron-common
Requires:       python-UcsSdk
Requires:       python-ncclient
Requires:       python-lxml

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
This package contains %{drv_vendor} networking driver for OpenStack Neutron.

%prep
%setup -q -n %{package_name}-%{upstream_version}

%build
%{__python2} setup.py build
%{__python2} setup.py build_sphinx
rm %{docpath}/.buildinfo

%install
export PBR_VERSION=%{version}
export SKIP_PIP_INSTALL=1
%{__python2} setup.py install --skip-build --root %{buildroot}
install -d -m 755 %{buildroot}%{_sysconfdir}/neutron/
mv %{buildroot}/usr/etc/neutron/*.ini %{buildroot}%{_sysconfdir}/neutron/

# Install systemd units
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/neutron-cisco-cfg-agent.service

mkdir -p %{buildroot}/%{_sysconfdir}/neutron/conf.d/neutron-cisco-cfg-agent

%files
%license LICENSE
%doc README.rst
%doc %{docpath}
%{python2_sitelib}/%{srcname}
%{python2_sitelib}/%{srcname}-%{version}-py%{python2_version}.egg-info
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/*.ini
%{_bindir}/neutron-cisco-cfg-agent
%{_unitdir}/neutron-cisco-cfg-agent.service

%post
%systemd_post neutron-cisco-cfg-agent.service

%preun
%systemd_preun neutron-cisco-cfg-agent.service

%postun
%systemd_postun_with_restart neutron-cisco-cfg-agent.service

%changelog
