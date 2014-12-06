#
# Conditional build:
%bcond_with	tests	# make check (requires BES server)
#
Summary:	OPeNDAP server module to return a GeoTiff, JP2k, etc., file for a DAP Data response
Summary(pl.UTF-8):	Moduł serwera OPeNDAP zwracający pliki GeoTiff, JP2k itp. jako odpowiedź DAP
Name:		opendap-fileout_gdal
Version:	0.9.4
Release:	1
License:	LGPL v2.1+
Group:		Daemons
Source0:	http://www.opendap.org/pub/source/fileout_gdal-%{version}.tar.gz
# Source0-md5:	85428b7c475f4cbd8b79e28aaba0bfd0
Patch0:		%{name}-includes.patch
URL:		http://opendap.org/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake >= 1:1.10
%{?with_tests:BuildRequires:	bes >= 3.13.0}
BuildRequires:	bes-devel >= 3.13.0
BuildRequires:	gdal-devel >= 1.9.0
BuildRequires:	libdap-devel >= 3.13.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	pkgconfig
Requires:	bes >= 3.13.0
Requires:	gdal >= 1.9.0
Requires:	libdap >= 3.13.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the fileout GDAL response handler for Hyrax - the OPeNDAP data
server. With this handler a server can easily be configured to return
data packaged in a GeoTiff, JP2, etc., file.

%description -l pl.UTF-8
Ten pakiet zawiera moduł serwera danych OPeNDAP (Hyrax) obsługujący
odpowiedzi fileout GDAL. Przy jego użyciu można łatwo skonfigurować
serwer, aby zwracał dane spakowane w pliku GeoTiff, JP2 itp.

%prep
%setup -q -n fileout_gdal-%{version}
%patch0 -p1

%build
# rebuild autotools for -as-needed to work
%{__libtoolize}
%{__aclocal} -I conf
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-openjpeg-prefix=/usr
%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/bes/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog NEWS README
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bes/modules/fong.conf
%attr(755,root,root) %{_libdir}/bes/libfong_module.so
