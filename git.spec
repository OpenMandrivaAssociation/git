%global __requires_exclude perl\\(packed-refs\\)|funcoes/func.gammu.php
%global __provides_exclude_from %{_docdir}
%global __requires_exclude_from %{_docdir}

%define libname %mklibname git
%define profile_branch 93git-branch.sh
%define profile_env 93git-env.sh
%bcond_without docs

#define beta rc2

Summary:	Global Information Tracker
Name:		git
Version:	2.50.1
Release:	%{?beta:0.%{beta}.}1
License:	GPLv2
Group:		Development/Other
Url:		https://git-scm.com/
Source0:	https://www.kernel.org/pub/software/scm/git/%{?beta:testing/}%{name}-%{version}%{?beta:.%{beta}}.tar.xz
Source2:	gitweb.conf
Source3:	%{profile_branch}
# Do we really need it? It's not used anyway
Source4:	%{profile_env}
Source5:	git.service
Source6:	git.socket

BuildRequires:	asciidoc
BuildRequires:	perl-CGI
BuildRequires:	gettext
%if %{with docs}
BuildRequires:	xmlto
BuildRequires:	docbook-dtd45-xml
%endif
BuildRequires:	systemd
BuildRequires:	perl-devel
BuildRequires:	perl(JSON::PP)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(zlib)

Requires:	git-core = %{EVRD}
Suggests:	gitk = %{EVRD}
Suggests:	git-svn = %{EVRD}
Suggests:	git-email = %{EVRD}
Suggests:	git-scalar = %{EVRD}
Suggests:	git-arch = %{EVRD}
Suggests:	git-cvs = %{EVRD}

%patchlist
git-1.8-do-not-use-hardcoded-defs.patch
gitk_tcl9_fix.patch 
port_git_gui_to_tcl_9.patch 

%description
This is a stupid (but extremely fast) directory content manager.  It
doesn't do a whole lot, but what it _does_ do is track directory
contents efficiently. It is intended to be the base of an efficient,
distributed source code management system. This package includes
rudimentary tools that can be used as a SCM, but you should look
elsewhere for tools for ordinary humans layered on top of this.

This is a dummy package which brings in all subpackages.

%package -n task-git
Summary:	Full git suite
Group:		Development/Other
Requires:	git = %{EVRD}
Requires:	git-core = %{EVRD}
Suggests:	gitk = %{EVRD}
Suggests:	git-svn = %{EVRD}
Suggests:	git-email = %{EVRD}
Suggests:	git-scalar = %{EVRD}
Suggests:	git-arch = %{EVRD}
Suggests:	git-core-oldies = %{EVRD}
Suggests:	git-cvs = %{EVRD}
Suggests:	git-daemon = %{EVRD}
Suggests:	git-prompt = %{EVRD}
Suggests:	gitweb = %{EVRD}
Suggests:	perl-Git = %{EVRD}
Suggests:	perl-Git-SVN = %{EVRD}

%description -n task-git
Full git suite.

%package core
Summary:	Global Information Tracker
Group:		Development/Other
Requires:	diffutils
Requires:	rsync
Requires:	less
Requires:	openssh-clients
Suggests:	git-prompt
# Abandoned and dropped in 2.12
Obsoletes:	gitview < %{EVRD}
Obsoletes:	git-core-oldies < %{EVRD}

%description core
This is a stupid (but extremely fast) directory content manager.  It
doesn't do a whole lot, but what it _does_ do is track directory
contents efficiently. It is intended to be the base of an efficient,
distributed source code management system. This package includes
rudimentary tools that can be used as a SCM, but you should look
elsewhere for tools for ordinary humans layered on top of this.

This are the core tools with minimal dependencies.

You may want to install subversion, cpsps and/or tla to import
repositories from other VCS.

%package extras
Summary:	Additional tools, scripts documentation for working with git
Group:		Development/Other
Requires:	git-core = %{EVRD}

%description extras
Additional tools,scripts and documentation for working with git

%package -n gitk
Summary:	Git revision tree visualiser
Group:		Development/Other
Requires:	git-core = %{EVRD}
Requires:	tk >= 8.6
Requires:	tcl >= 8.6

%description -n gitk
Git revision tree visualiser.

%package -n %{libname}-devel
Summary:	Git development files
Group:		Development/Other
Provides:	git-devel = %{version}-%{release}

%description -n %{libname}-devel
Development files for git.

%package svn
Summary:	Git tools for importing Subversion repositories
Group:		Development/Other
Requires:	git-core = %{EVRD}
Requires:	subversion
Requires:	perl-Git-SVN

%description svn
Git tools for importing Subversion repositories.

%package cvs
Summary:	Git tools for importing CVS repositories
Group:		Development/Other
Requires:	git-core = %{EVRD}
Suggests:	cvs
Suggests:	cvsps

%description cvs
Git tools for importing CVS repositories.

%package arch
Summary:	Git tools for importing Arch repositories
Group:		Development/Other
Requires:	git-core = %{EVRD}
Suggests:	tla

%description arch
Git tools for importing Arch repositories.

%package email
Summary:	Git tools for sending email
Group:		Development/Other
Requires:	git-core = %{EVRD}
# (tpg) these days SSL is widely used by email providers
Requires:	perl(Net::SMTP::SSL)
Requires:	perl(Authen::SASL)
Requires:	perl(MIME::Base64)

%description email
Git tools for sending email.

%package scalar
Summary:	Tools for git scalability
Group:		Development/Tools
Requires:	git-core = %{EVRD}

%description scalar
Scalar is a tool that helps Git scale to some of the largest Git repositories.
It achieves this by enabling some advanced Git features, such as:

* Partial clone: reduces time to get a working repository by not downloading
  all Git objects right away.

* Background prefetch: downloads Git object data from all remotes every
  hour, reducing the amount of time for foreground git fetch calls.

* Sparse-checkout: limits the size of your working directory.

* File system monitor: tracks the recently modified files and eliminates
  the need for Git to scan the entire worktree.

* Commit-graph: accelerates commit walks and reachability calculations,
  speeding up commands like git log.

* Multi-pack-index: enables fast object lookups across many pack-files.

* Incremental repack: Repacks the packed Git data into fewer pack-file
  without disrupting concurrent commands by using the multi-pack-index.


%package -n perl-Git
Summary:	Perl interface to Git
Group:		Development/Perl
Requires:	git-core = %{EVRD}

%description -n perl-Git
Perl interface to Git.

%package -n perl-Git-SVN
Summary:	Perl interface to Git SVN
Group:		Development/Perl
Requires:	perl-Git = %{EVRD}

%description -n perl-Git-SVN
Perl interface to Git SVN.

#--------------
# Remove remote-helper python libraries and scripts, these are not ready for
# use yet
#--------------

%package -n gitweb
Summary:	cgi-bin script for browse a git repository with web browser
Group:		System/Servers
Requires:	git-core = %{EVRD}
Suggests:	apache-mod_socache_shmcb

%description -n gitweb
cgi-bin script for browse a git repository with web browser.

%package prompt
Summary:	Shows the current git branch in your bash prompt
Group:		Shells
Requires:	git-core = %{EVRD}
Requires:	bash-completion

%description prompt
Shows the current git branch in your bash prompt.

%package server
Summary:	git:// protocol server
Group:		System/Servers
Requires:	git-core = %{EVRD}
%systemd_requires
%rename git-daemon

%description server
The git daemon for supporting git:// access to git repositories.

%prep
%autosetup -p1 -n %{name}-%{version}%{?beta:.%{beta}}
# remove boring file
rm -f Documentation/.gitignore
# prefix gitweb css/png files with /gitweb
perl -pi -e 's!^(GITWEB_CSS|GITWEB_LOGO|GITWEB_FAVICON) = !$1 = /gitweb/!' Makefile
sed -i 's!make CC=clang CXX=clang++!make CC=%{__cc} CXX=%{__cxx}!g' Makefile

%build
# same flags and prefix must be passed for make test too
%define git_make_params prefix=%{_prefix} CC=%{__cc} gitexecdir=%{_libdir}/git-core CFLAGS="%{optflags}" GITWEB_CONFIG=%{_sysconfdir}/gitweb.conf DOCBOOK_XSL_172=0 INSTALLDIRS=vendor perllibdir=%{perl_vendorlib}
%make CC=%{__cc} AR=%{__ar} %{git_make_params} all %{?with_docs:doc}

# Produce RelNotes.adoc.xz
# sed trick changes "-x.y.z.adoc" to "-x.y.z.0.adoc" for ordering, then undoes it
# use awk to print a newline before each RelNotes header
cd Documentation/RelNotes \
&& relnotesls="`find . -name '*.adoc' | sed 's/\([0-9]\.[0-9]\.[0-9]\)\.adoc/\1.0.adoc/' | sort -nr | sed 's/\([0-9]\.[0-9]\.[0-9]\)\.0\.adoc/\1.adoc/'`" \
&& awk 'FNR == 1 { print "" } { print }' $relnotesls | xz -9ec >../RelNotes.adoc.xz

%install
mkdir -p %{buildroot}%{_bindir}
%make_install %{?with_docs:install-doc} CC=%{__cc} AR=%{__ar} prefix=%{_prefix} gitexecdir=%{_libdir}/git-core  CFLAGS="%{optflags}" INSTALLDIRS=vendor perllibdir=%{perl_vendorlib}

# Contrib contains some useful stuff -- let's package it in git-extras
cp -a contrib/git-resurrect.sh %{buildroot}%{_bindir}/git-resurrect
cp -a contrib/git-jump/git-jump %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_docdir}/git-extras
# Avoid dependencies on obscure perl modules
find contrib -name "*.pl" -o -name "*.perl" |xargs chmod -x
cp -ar contrib %{buildroot}%{_docdir}/git-extras

mkdir -p %{buildroot}%{_includedir}/git
cp *.h %{buildroot}%{_includedir}/git

mkdir -p %{buildroot}%{_libdir}
install -m 644 libgit.a %{buildroot}%{_libdir}/libgit.a

[ -d %{buildroot}%{_prefix}/lib/perl5/site_perl ] && mv %{buildroot}/%{_prefix}/lib/perl5/site_perl %{buildroot}/%{_prefix}/lib/perl5/vendor_perl
rm -f %{buildroot}/%{perl_vendorlib}/Error.pm

mkdir -p %{buildroot}%{_datadir}/gitweb/static
install -m 755 gitweb/gitweb.cgi %{buildroot}%{_datadir}/gitweb
install -m 644 gitweb/static/*.css gitweb/static/*.png %{buildroot}%{_datadir}/gitweb/static/

mkdir -p %{buildroot}%{_unitdir}
install -m 644 %{SOURCE5} %{buildroot}%{_unitdir}
install -m 644 %{SOURCE6} %{buildroot}%{_unitdir}

mkdir -p %{buildroot}%{_sysconfdir}
install -m644 %{SOURCE2} %{buildroot}%{_sysconfdir}/gitweb.conf
# apache configuration
mkdir -p %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/gitweb.conf <<EOF
# gitweb configuration
Alias /gitweb %{_datadir}/gitweb

<Directory %{_datadir}/gitweb>
    Require all granted
    Options ExecCgi
    DirectoryIndex gitweb.cgi
    AddHandler cgi-script .cgi
</Directory>
EOF

# fix .sp in man files
find %{buildroot}/%{_mandir} -type f | xargs perl -e 's/\.sp$/\n\.sp/g' -pi

# emacs VC backend:
mkdir -p %{buildroot}{%{_datadir}/emacs/site-lisp,/etc/emacs/site-start.d}
install -m 644 contrib/emacs/*.el %{buildroot}%{_datadir}/emacs/site-lisp
cat >%{buildroot}/etc/emacs/site-start.d/vc_git.el <<EOF
(add-to-list 'vc-handled-backends 'GIT)
EOF

# install bash-completion file
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
install -m644 contrib/completion/git-completion.bash \
    %{buildroot}%{_sysconfdir}/bash_completion.d/git

# And the prompt manipulation file
install -D -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/profile.d/%{profile_branch}

# exposes a bug in less, as reported by coling
#install -D -m 0644 %SOURCE4 %{buildroot}%{_sysconfdir}/profile.d/%{profile_env}

# Sometimes created, sometimes not -- its presence actually seems to be
# an indication of a random error while building man pages
rm -f %{buildroot}%{_mandir}/man3/private-Error.3*

cp -a contrib/workdir/git-new-workdir %{buildroot}%{_bindir}/

%find_lang %{name}

%check
# We do NO_SVN_TESTS because git's tests hardcode
# replies from svn versions older than the one
# we're shipping -- and they have changed since
if ! LC_ALL=C %make %{git_make_params} test NO_SVN_TESTS=true; then
    printf '%s\n' "WARNING: Some tests failed. You may want to investigate."
fi

%post server
%systemd_post git.socket

%preun server
%systemd_preun git.socket

%postun server
%systemd_postun_with_restart git.socket

%files
# no file in the main package

%files -n task-git
# no file in this package

%files core -f %{name}.lang
/etc/emacs/site-start.d/*
/etc/bash_completion.d/*
%{_datadir}/bash-completion/completions/git
%{_datadir}/emacs/site-lisp/*
%{_bindir}/git
%{_bindir}/git-new-workdir
%{_bindir}/git-receive-pack
%{_bindir}/git-upload-archive
%{_bindir}/git-upload-pack
%{_libdir}/git-core
%exclude %{_libdir}/git-core/*svn*
%exclude %{_libdir}/git-core/*cvs*
%exclude %{_libdir}/git-core/git-archimport
%exclude %{_libdir}/git-core/*email*
%exclude %{_libdir}/git-core/git-citool
%exclude %{_libdir}/git-core/git-gui
%exclude %{_libdir}/git-core/git-instaweb
%exclude %{_libdir}/git-core/git-filter-branch
%exclude %{_libdir}/git-core/git-request-pull
%{_datadir}/git-core
%exclude %{_datadir}/git-core/templates/hooks/fsmonitor-watchman.sample
%exclude %{_datadir}/git-core/templates/hooks/pre-rebase.sample
%exclude %{_datadir}/git-core/templates/hooks/prepare-commit-msg.sample
%if %{with docs}
%doc %{_mandir}/man1/git*.1*
%exclude %{_mandir}/man1/*archimport*.1*
%exclude %{_mandir}/man1/*cvs*.1*
%exclude %{_mandir}/man1/*email*.1*
%exclude %{_mandir}/man1/gitweb.1*
%doc %{_mandir}/man5/*
%exclude %{_mandir}/man5/gitweb.conf.*
%doc %{_mandir}/man7/*
%endif

%files -n gitk
%{_bindir}/gitk
%{_libdir}/git-core/git-citool
%{_libdir}/git-core/git-gui
%if %{with docs}
%doc %{_mandir}/*/gitk*
%endif
%{_datadir}/gitk
%{_datadir}/git-gui

%files -n %{libname}-devel
%{_includedir}/git
%{_libdir}/libgit.a

%files svn
%{_libdir}/git-core/*svn*
%if %{with docs}
%doc %{_mandir}/man1/*svn*.1*
%endif

%files cvs
%{_bindir}/git-cvsserver
%{_libdir}/git-core/*cvs*

%if %{with docs}
%doc %{_mandir}/man1/*cvs*.1*
%doc %{_mandir}/man7/*cvs*.7*
%endif

%files arch
%{_libdir}/git-core/git-archimport
%if %{with docs}
%doc %{_mandir}/man1/git-archimport.1*
%endif

%files email
%{_libdir}/git-core/*email*
%if %{with docs}
%doc %{_mandir}/man1/*email*.1*
%endif

%files scalar
%{_bindir}/scalar
%if %{with docs}
%doc %{_mandir}/man1/scalar.1*
%endif

%files -n perl-Git
%{perl_vendorlib}/Git.pm
%dir %{perl_vendorlib}/Git
%{perl_vendorlib}/Git/I18N.pm
%{perl_vendorlib}/Git/IndexInfo.pm
%{perl_vendorlib}/Git/Packet.pm
%{perl_vendorlib}/FromCPAN
%{perl_vendorlib}/Git/LoadCPAN.pm
%{perl_vendorlib}/Git/LoadCPAN
%if %{with docs}
%doc %{_mandir}/man3/Git.3pm*
%endif

%files -n perl-Git-SVN
%{perl_vendorlib}/Git/SVN
%{perl_vendorlib}/Git/SVN.pm

%files -n gitweb
%doc gitweb/INSTALL
%config(noreplace) %{_sysconfdir}/gitweb.conf
%config(noreplace) %{_webappconfdir}/gitweb.conf
%{_libdir}/git-core/git-instaweb
%{_datadir}/gitweb
%if %{with docs}
%doc %{_mandir}/man1/gitweb.1*
%doc %{_mandir}/man5/gitweb.conf.5*
%endif

%files prompt
%{_sysconfdir}/profile.d/%{profile_branch}

%files server
%{_bindir}/git-shell
%{_unitdir}/git.service
%{_unitdir}/git.socket

%files extras
%if %{with docs}
%doc Documentation/*.html Documentation/howto Documentation/technical Documentation/RelNotes.adoc.xz
%endif
%doc %{_docdir}/git-extras/contrib
%{_bindir}/git-resurrect
%{_bindir}/git-jump
%{_libdir}/git-core/git-filter-branch
%{_libdir}/git-core/git-request-pull
%{_datadir}/git-core/templates/hooks/fsmonitor-watchman.sample
%{_datadir}/git-core/templates/hooks/pre-rebase.sample
%{_datadir}/git-core/templates/hooks/prepare-commit-msg.sample
