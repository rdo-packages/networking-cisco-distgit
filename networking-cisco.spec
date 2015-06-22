%define name networking-cisco
%define version 2015.1.1.dev6
%define unmangled_version 2015.1.1.dev6
%define unmangled_version 2015.1.1.dev6
%define release 1

Summary: Networking Cisco contains the Cisco vendor code for Openstack Neutron
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: UNKNOWN
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Cisco Systems <openstack-networking@cisco.com>
Url: https://github.com/openstack/networking-cisco

%description
===============================
networking-cisco
===============================

Networking Cisco contains the Cisco vendor code for Openstack Neutron

* Free software: Apache license
* Documentation: http://docs.openstack.org/developer/networking-cisco
* Source: http://git.openstack.org/cgit/openstack/networking-cisco
* Bugs: http://bugs.launchpad.net/networking-cisco

Features
--------

* TODO



%prep
%setup -n %{name}-%{unmangled_version} -n %{name}-%{unmangled_version}

%build
python setup.py build

%install
python setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
