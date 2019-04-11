# The lsb release used in the tarball name
%global lsb 1lsb3.2
# Not defined on el6
%{!?_cups_serverbin: %global _cups_serverbin %(/usr/bin/cups-config --serverbin)}

Name:           epson-inkjet-printer-escpr
Summary:        Drivers for Epson inkjet printers
Version:        1.6.38
Release:        1.%{lsb}
License:        GPLv2+
URL:            http://download.ebz.epson.net/dsc/search/01/search/?OSC=LX
# Download address is garbled on web page
Source0:        https://download3.ebz.epson.net/dsc/f/03/00/08/18/20/e94de600e28e510c1cfa158929d8b2c0aadc8aa0/epson-inkjet-printer-escpr-%{version}-%{lsb}.tar.gz
# Fix includes
#Patch0:         epson-inkjet-printer-escpr-inc.patch
# Patch from Arch Linux
# https://aur.archlinux.org/packages/epson-inkjet-printer-escpr/
#Patch1:         epson-inkjet-printer-escpr-filter.patch

BuildRequires:  autoconf
BuildRequires:  chrpath
BuildRequires:  cups-devel
BuildRequires:  pkgconfig(libjpeg)

# For automatic detection of printer drivers
BuildRequires:  python-cups
# For dir ownership
Requires:       cups

%description
This package contains drivers for Epson Inkjet printers that use 
the New Generation Epson Printer Control Language.

For a detailed list of supported printers, please refer to
http://avasys.jp/english/linux_e/

%prep
%setup -q 
#%patch0 -p1 -b .inc
#%patch1 -p1 -b .filter
# Fix permissions
find . -name \*.h -exec chmod 644 {} \;
find . -name \*.c -exec chmod 644 {} \;
for f in README README.ja COPYING AUTHORS NEWS; do
 chmod 644 $f
done

%build
autoconf
%configure --disable-static --enable-shared --disable-rpath
# SMP make doesn't work
#make %{?_smp_mflags}
make

%install
make install DESTDIR=%{buildroot} CUPS_PPD_DIR=%{_datadir}/ppd/Epson
# Get rid of .la files
rm -f %{buildroot}%{_libdir}/*.la
# Compress ppd files
for ppd in %{buildroot}%{_datadir}/ppd/Epson/epson-inkjet-printer-escpr/*.ppd; do
 gzip $ppd
done
# Get rid of rpath
chrpath --delete %{buildroot}%{_cups_serverbin}/filter/epson-escpr
# Copy documentation
cp -a README README.ja COPYING AUTHORS NEWS ..

# Get rid of .so file, since no headers are installed.
rm %{buildroot}%{_libdir}/libescpr.so

#%ldconfig_scriptlets

%files
%doc README README.ja COPYING AUTHORS NEWS
%{_cups_serverbin}/filter/epson-*
%{_datadir}/ppd/Epson/
%{_libdir}/libescpr.so.*
