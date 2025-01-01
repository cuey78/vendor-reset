%global debug_package %{nil}
%global dkms_name vendor-reset

Name:       %{dkms_name}-dkms
Version:    0.0.git.118.92b8d308
Release:    1%{?dist}
Summary:    Linux kernel vendor specific hardware reset module
License:    GPLv2
URL:        https://github.com/cuey78/vendor-reset
BuildArch:  noarch

# Define the source archive URL
Source:     https://github.com/cuey78/vendor-reset/archive/refs/heads/master.zip

# Provide information about the package
Provides:   %{dkms_name}-dkms = %{version}
Requires:   dkms

%description
A kernel module that is capable of resetting hardware devices into a state where they can be re-initialized or passed through into a virtual machine (VFIO).

# Empty changelog section to satisfy RPM requirements
%changelog

%prep
# Ensure the correct source directory name and extract
%setup -q -n vendor-reset-0.1.0

%build
# Typically, DKMS modules don't require a separate build step in the spec file
# Add build commands here if needed, although usually omitted for DKMS-based packages

%install
# Create necessary directories and install files into the build root
# Example: creating configuration files or directories
install -d %{buildroot}%{_sysconfdir}/modules-load.d
cat > %{buildroot}%{_sysconfdir}/modules-load.d/vendor-reset.conf << EOF
vendor-reset
EOF

%post -n %{name}
# Post-installation commands (e.g., adding to DKMS)
dkms add -m %{dkms_name} -v %{version} -q || :
dkms build -m %{dkms_name} -v %{version} -q || :
dkms install -m %{dkms_name} -v %{version} -q --force || :

%preun
# Pre-uninstallation commands (e.g., removing from DKMS)
dkms remove -m %{dkms_name} -v %{version} -q --all || :

%files
# List of files to be included in the package
%license LICENSE
%doc README.md
%{_sysconfdir}/modules-load.d/vendor-reset.conf

# Optional: if there are no files to list in %changelog, it can be empty
%changelog
