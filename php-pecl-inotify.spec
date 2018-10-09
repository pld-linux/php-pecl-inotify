%define		php_name	php%{?php_suffix}
%define		modname	inotify
%define		status		stable
Summary:	%{modname} - php bindings
Summary(pl.UTF-8):	%{modname} - dowiązania php
Name:		%{php_name}-pecl-%{modname}
Version:	2.0.0
Release:	1
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	f7a951b3c66d08f5e7889479f5fc7564
URL:		http://pecl.php.net/package/inotify/
BuildRequires:	%{php_name}-devel >= 3:5.0.4
BuildRequires:	glibc-devel >= 6:2.3.6-19
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Provides:	php(%{modname}) = %{version}
Obsoletes:	php-pecl-inotify < 0.1.6-5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The inotify extension allows to use inotify functions in a PHP script.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
Rozszerzenie inotify pozwala na skorzystanie z funkcji inotify w
skrypcie PHP.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -p inotify.php tail.php $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc CREDITS EXPERIMENTAL README
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
%{_examplesdir}/%{name}-%{version}
