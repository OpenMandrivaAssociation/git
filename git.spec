%global __requires_exclude perl\\(packed-refs\\)|funcoes/func.gammu.php
%global __provides_exclude_from %{_docdir}
%global __requires_exclude_from %{_docdir}

%define libname %mklibname git
%define profile_branch 93git-branch.sh
%define profile_env 93git-env.sh

Summary:	Global Information Tracker
Name:		git
Epoch:		1
Version:	2.17.0
Release:	1
License:	GPLv2
Group:		Development/Other
Url:		http://git-scm.com/
Source0:	https://www.kernel.org/pub/software/scm/git/%{name}-%{version}.tar.xz
Source2:	gitweb.conf
Source3:	%{profile_branch}
# Do we really need it? It's not used anyway
Source4:	%{profile_env}
Patch0:		git-1.8-do-not-use-hardcoded-defs.patch
Source5:	git.service
Source6:	git.socket

BuildRequires:	asciidoc
BuildRequires:	docbook-dtd45-xml
BuildRequires:	perl-CGI
BuildRequires:	xmlto
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
Suggests:	git-arch = %{EVRD}
Suggests:	git-cvs = %{EVRD}

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
Requires:	gitk = %{EVRD}
Suggests:	git-svn = %{EVRD}
Requires:	git-email = %{EVRD}
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
Conflicts:	git-core < 1:2.16.3-4

%description extras
Additional tools,scripts and documentation for working with git

%package -n gitk
Summary:	Git revision tree visualiser
Group:		Development/Other
Requires:	git-core = %{EVRD}
Requires:	tk >= 8.4
Requires:	tcl >= 8.4

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
Suggests:	perl-Authen-SASL
Suggests:	perl-MIME-Base64

%description email
Git tools for sending email.

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
Requires(preun,post,postun):	rpm-helper
%rename git-daemon

%description server
The git daemon for supporting git:// access to git repositories.

%prep
%setup -q
# remove boring file
rm -f Documentation/.gitignore
# prefix gitweb css/png files with /gitweb
perl -pi -e 's!^(GITWEB_CSS|GITWEB_LOGO|GITWEB_FAVICON) = !$1 = /gitweb/!' Makefile
%apply_patches

%build
# same flags and prefix must be passed for make test too
%define git_make_params prefix=%{_prefix} CC=%{__cc} gitexecdir=%{_libdir}/git-core CFLAGS="%{optflags}" GITWEB_CONFIG=%{_sysconfdir}/gitweb.conf DOCBOOK_XSL_172=1 INSTALLDIRS=vendor perllibdir=%{perl_vendorlib}
%make CC=%{__cc} AR=%{__ar} %{git_make_params} all doc

# Produce RelNotes.txt.gz
# sed trick changes "-x.y.z.txt" to "-x.y.z.0.txt" for ordering, then undoes it
# use awk to print a newline before each RelNotes header
cd Documentation/RelNotes \
&& relnotesls="`find . -name '*.txt' | sed 's/\([0-9]\.[0-9]\.[0-9]\)\.txt/\1.0.txt/' | sort -nr | sed 's/\([0-9]\.[0-9]\.[0-9]\)\.0\.txt/\1.txt/'`" \
&& awk 'FNR == 1 { print "" } { print }' $relnotesls | gzip -9c >../RelNotes.txt.gz

%install
mkdir -p %{buildroot}%{_bindir}
%make_install CC=%{__cc} AR=%{__ar} prefix=%{_prefix} gitexecdir=%{_libdir}/git-core  CFLAGS="%{optflags}" INSTALLDIRS=vendor perllibdir=%{perl_vendorlib}
make install-doc CC=%{__cc} AR=%{__ar} prefix=%{_prefix} gitexecdir=%{_libdir}/git-core   DESTDIR=%{buildroot}

# Contrib contains some useful stuff -- let's package it in git-extras
mv contrib/git-resurrect.sh %{buildroot}%{_bindir}/git-resurrect
mv contrib/git-jump/git-jump %{buildroot}%{_bindir}/
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

mv contrib/workdir/git-new-workdir %{buildroot}%{_bindir}/

%find_lang %{name}

%check
# We do NO_SVN_TESTS because git's tests hardcode
# replies from svn versions older than the one
# we're shipping -- and they have changed since
if ! LC_ALL=C %make %{git_make_params} test NO_SVN_TESTS=true; then
    printf '%s\n' "WARNING: Some tests failed. You may want to investigate."
fi

%files
# no file in the main package

%files -n task-git
# no file in this package

%files core -f %{name}.lang
/etc/emacs/site-start.d/*
/etc/bash_completion.d/*
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
%exclude %{_libdir}/git-core/git-add--interactive
%exclude %{_libdir}/git-core/git-filter-branch
%exclude %{_libdir}/git-core/git-request-pull
%{_datadir}/git-core
%exclude %{_datadir}/git-core/templates/hooks/fsmonitor-watchman.sample
%exclude %{_datadir}/git-core/templates/hooks/pre-rebase.sample
%exclude %{_datadir}/git-core/templates/hooks/prepare-commit-msg.sample
%exclude %{_mandir}/man1/*svn*.1*
%exclude %{_mandir}/man1/*cvs*.1*
%exclude %{_mandir}/man7/*cvs*.7*
%exclude %{_mandir}/man1/*email*.1*
%exclude %{_mandir}/man1/git-archimport.1*

%files -n gitk
%{_bindir}/gitk
%{_libdir}/git-core/git-citool
%{_libdir}/git-core/git-gui
%{_mandir}/*/gitk*
%{_datadir}/gitk
%{_datadir}/git-gui

%files -n %{libname}-devel
%{_includedir}/git
%{_libdir}/libgit.a

%files svn
%{_libdir}/git-core/*svn*
%{_mandir}/man1/*svn*.1*

%files cvs
%{_bindir}/git-cvsserver
%{_libdir}/git-core/*cvs*
%{_mandir}/man1/*cvs*.1*
%{_mandir}/man7/*cvs*.7*

%files arch
%{_libdir}/git-core/git-archimport
%{_mandir}/man1/git-archimport.1*

%files email
%{_libdir}/git-core/*email*
%{_mandir}/man1/*email*.1*

%files -n perl-Git
%{perl_vendorlib}/Git.pm
%dir %{perl_vendorlib}/Git
%{perl_vendorlib}/Git/I18N.pm
%{perl_vendorlib}/Git/IndexInfo.pm
%{perl_vendorlib}/Git/Packet.pm
%{perl_vendorlib}/FromCPAN
%{perl_vendorlib}/Git/LoadCPAN.pm
%{perl_vendorlib}/Git/LoadCPAN
%{_mandir}/man3/Git.3pm*

%files -n perl-Git-SVN
%{perl_vendorlib}/Git/SVN
%{perl_vendorlib}/Git/SVN.pm

%files -n gitweb
%doc gitweb/INSTALL
%config(noreplace) %{_sysconfdir}/gitweb.conf
%config(noreplace) %{_webappconfdir}/gitweb.conf
%{_libdir}/git-core/git-instaweb
%{_datadir}/gitweb
%{_mandir}/man1/gitweb.1*
%{_mandir}/man5/gitweb.conf.5*

%files prompt
%{_sysconfdir}/profile.d/%{profile_branch}

%files server
%{_bindir}/git-shell
%{_unitdir}/git.service
%{_unitdir}/git.socket

%files extras
%doc Documentation/*.html Documentation/howto Documentation/technical Documentation/RelNotes.txt.gz
%doc %{_docdir}/git-extras
%{_bindir}/git-resurrect
%{_bindir}/git-jump
%{_libdir}/git-core/git-add--interactive
%{_libdir}/git-core/git-filter-branch
%{_libdir}/git-core/git-request-pull
%{_datadir}/git-core/templates/hooks/fsmonitor-watchman.sample
%{_datadir}/git-core/templates/hooks/pre-rebase.sample
%{_datadir}/git-core/templates/hooks/prepare-commit-msg.sample
%{_mandir}/*/git-*
%{_mandir}/*/git.*
%{_mandir}/*/gitattributes*
%{_mandir}/*/gitignore*
%{_mandir}/*/gitmodules*
%{_mandir}/*/gitnamespaces*
%{_mandir}/*/gitcli*
%{_mandir}/*/giteveryday*
%{_mandir}/*/githooks*
%{_mandir}/*/gitrepository*
%{_mandir}/*/*tutorial*
%{_mandir}/*/*glossary*
%{_mandir}/*/gitdiffcore*
%{_mandir}/*/gitworkflows*
%{_mandir}/*/gitrevisions*
%{_mandir}/*/gitcredentials*
%{_mandir}/*/gitremote-helpers*
%{_mandir}/man7/*submodule*
