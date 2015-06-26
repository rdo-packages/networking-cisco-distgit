%global service networking-cisco

Name: openstack-%{service}
Version:    XXX
Release:    XXX{?dist}
Summary: Networking Cisco contains the Cisco vendor code for Openstack Neutron

Group: Development/Libraries
License: ASL 2.0
Vendor: Cisco Systems <openstack-networking@cisco.com>
Url: http://docs.openstack.org/developer/%{service}

BuildRoot: %{_tmppath}/%{service}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch

Source0: http://tarballs.openstack.org/%{service}/%{service}-master.tar.gz
Source1:	neutron-cisco-cfg-agent.service

%description
Networking Cisco contains the Cisco vendor code for Openstack Neutron
* Documentation: http://docs.openstack.org/developer/%{service}
* Source: http://git.openstack.org/cgit/openstack/%{service}
* Bugs: http://bugs.launchpad.net/%{service}


%prep
%setup -q -n %{service}-%{upstream_version}

%build
python setup.py build

%install
python setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

# Install systemd units
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/neutron-cisco-cfg-agent.service

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%license LICENSE
%doc networking_cisco/plugins/cisco/README
%{_unitdir}/neutron-cisco-cfg-agent.service
%defattr(-,root,root)


%preun
%systemd_preun neutron-cisco-cfg-agent.service


%postun
%systemd_postun_with_restart neutron-cisco-cfg-agent.service
