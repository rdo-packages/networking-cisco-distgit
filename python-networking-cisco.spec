%global drv_vendor Cisco
%global srcname networking_cisco
%global package_name networking-cisco
%global docpath doc/build/html

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-%{package_name}
Epoch:          1
Version:        XXX
Release:        XXX
Summary:        %{drv_vendor} OpenStack Neutron driver

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/%{package_name}
Source0:        https://tarballs.openstack.org/%{package_name}/%{package_name}-%{version}.tar.gz
Source1:        neutron-cisco-cfg-agent.service

BuildArch:      noarch
BuildRequires:  git
BuildRequires:  python2-devel
BuildRequires:  python-mock
BuildRequires:  python-neutron-tests
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx
BuildRequires:  python-testrepository
BuildRequires:  python-testtools
BuildRequires:  systemd-units

Requires:       python-babel
Requires:       python-pbr
Requires:       openstack-neutron-common
Requires:       python-neutron-lib >= 0.1.0
Requires:       python-oslo-concurrency >= 3.5.0
Requires:       python-oslo-config >= 2:3.7.0
Requires:       python-oslo-db >= 4.1.0
Requires:       python-oslo-i18n >= 2.1.0
Requires:       python-oslo-log >= 1.14.0
Requires:       python-oslo-messaging >= 4.0.0
Requires:       python-oslo-serialization >= 1.10.0
Requires:       python-oslo-service >= 1.0.0
Requires:       python-oslo-utils >= 3.5.0
Requires:       python-UcsSdk
Requires:       python-ncclient
Requires:       python-lxml
Requires:       python-neutron-tests

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
This package contains %{drv_vendor} networking driver for OpenStack Neutron.

%prep
%autosetup -n %{package_name}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f requirements.txt

# Kill egg-info in order to generate new SOURCES.txt
rm -rf networking_cisco.egg-info

%build
export SKIP_PIP_INSTALL=1
%{__python2} setup.py build
%{__python2} setup.py build_sphinx
rm %{docpath}/.buildinfo

%install
export PBR_VERSION=%{version}
export SKIP_PIP_INSTALL=1
%{__python2} setup.py install --skip-build --root %{buildroot}
install -d -m 755 %{buildroot}%{_sysconfdir}/neutron/
mv %{buildroot}/usr/etc/neutron/*.ini %{buildroot}%{_sysconfdir}/neutron/
install -d -m 755 %{buildroot}%{_sysconfdir}/saf/
mv %{buildroot}/usr/etc/saf/enabler_conf.ini %{buildroot}%{_sysconfdir}/saf/

# Install systemd units
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/neutron-cisco-cfg-agent.service
mv %{buildroot}/usr/etc/systemd/system/*.service %{buildroot}%{_unitdir}
mv %{buildroot}/usr/etc/saf/init/*.service %{buildroot}%{_unitdir}

# Remove upstart files, they are not needed
rm %{buildroot}/usr/etc/saf/init/*.conf
rm %{buildroot}/usr/etc/init/*.conf

# Move cpnr-rootwrap config files to its proper location
mkdir %{buildroot}%{_sysconfdir}/cpnr
mv %{buildroot}/usr/etc/cpnr/rootwrap.conf %{buildroot}%{_sysconfdir}/cpnr
mv %{buildroot}/usr/etc/cpnr/cisco_pnr.ini %{buildroot}%{_sysconfdir}/cpnr
mkdir -p %{buildroot}%{_datarootdir}/cpnr/rootwrap/
mv %{buildroot}/usr/usr/share/cpnr/rootwrap/cpnr.filters %{buildroot}%{_datarootdir}/cpnr/rootwrap/

mkdir -p %{buildroot}/%{_sysconfdir}/neutron/conf.d/neutron-cisco-cfg-agent

%files
%license LICENSE
%doc README.rst
%doc %{docpath}
%{python2_sitelib}/%{srcname}
%{python2_sitelib}/%{srcname}-%{version}-py%{python2_version}.egg-info
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/*.ini
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/saf/*.ini
%config(noreplace) %attr(0640, root, cpnr) %{_sysconfdir}/cpnr/*.conf
%config(noreplace) %attr(0640, root, cpnr) %{_sysconfdir}/cpnr/*.ini
%{_bindir}/neutron-cisco-cfg-agent
%{_bindir}/fabric-enabler-agent
%{_bindir}/fabric-enabler-cli
%{_bindir}/fabric-enabler-server
%{_bindir}/cpnr-dhcp-relay
%{_bindir}/cpnr-dns-relay
%{_bindir}/cpnr-dhcp-relay-agent
%{_bindir}/cpnr-dns-relay-agent
%{_bindir}/cpnr-rootwrap
%{_unitdir}/neutron-cisco-cfg-agent.service
%{_unitdir}/fabric-enabler-agent.service
%{_unitdir}/fabric-enabler-server.service
%{_unitdir}/cpnr-dhcp-relay.service
%{_unitdir}/cpnr-dns-relay.service
%{_datarootdir}/cpnr/

%pre
getent group cpnr >/dev/null || groupadd -r cpnr
getent passwd cpnr >/dev/null || \
    useradd -r -g cpnr -d %{_datarootdir}/cpnr -s /sbin/nologin \
    -c "OpenStack CPNR user for Cisco Networking" cpnr
exit 0

%post
%systemd_post neutron-cisco-cfg-agent.service
%systemd_post fabric-enabler-agent.service
%systemd_post fabric-enabler-server.service
%systemd_post cpnr-dns-relay.service
%systemd_post cpnr-dhdp-relay.service

%preun
%systemd_preun neutron-cisco-cfg-agent.service
%systemd_preun fabric-enabler-agent.service
%systemd_preun fabric-enabler-server.service
%systemd_preun cpnr-dns-relay.service
%systemd_preun cpnr-dhdp-relay.service

%postun
%systemd_postun_with_restart neutron-cisco-cfg-agent.service
%systemd_postun_with_restart fabric-enabler-agent.service
%systemd_postun_with_restart fabric-enabler-server.service
%systemd_postun_with_restart cpnr-dns-relay.service
%systemd_postun_with_restart cpnr-dhdp-relay.service

%changelog
