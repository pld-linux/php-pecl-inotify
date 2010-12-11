%define		_modname	inotify
%define		_status		beta
Summary:	%{_modname} - php bindings
Summary(pl.UTF-8):	%{_modname} - dowiązania php
Name:		php-pecl-%{_modname}
Version:	0.1.4
Release:	3
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	39b9a454e91f2ef525e1ed9862370517
URL:		http://pecl.php.net/package/inotify/
BuildRequires:	glibc-devel >= 6:2.4
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The inotify extension allows to use inotify functions in a PHP script.

In PECL status of this extension is: %{_status}.

%description -l pl.UTF-8
Rozszerzenie inotify pozwala na skorzystanie z funkcji inotify w
skrypcie PHP.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	-C %{_modname}-%{version} \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

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
%doc %{_modname}-%{version}/{CREDITS,EXPERIMENTAL,README,inotify.php,tail.php}
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
