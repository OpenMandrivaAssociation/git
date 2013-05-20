%define libname		%mklibname git
%define profile_branch	93git-branch.sh
%define profile_env	93git-env.sh

Summary:	Global Information Tracker
Name:		git
Epoch:		1
Version:	1.8.2.1
Release:	2
License:	GPLv2
Group:		Development/Other
Url:		http://git-scm.com/
Source0:	http://git-core.googlecode.com/files/%{name}-%{version}.tar.gz
Source2:	gitweb.conf
Source3:	%{profile_branch}
# Do we really need it? It's not used anyway
Source4:	%{profile_env}
Patch0:		git-1.8-do-not-use-hardcoded-defs.patch

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
Requires:	gitk = %{EVRD}
Requires:	git-svn = %{EVRD}
Requires:	git-email = %{EVRD}
Suggests:	git-arch = %{EVRD}
Suggests:	git-core-oldies = %{EVRD}
Suggests:	git-cvs = %{EVRD}

%description
This is a stupid (but extremely fast) directory content manager.  It
doesn't do a whole lot, but what it _does_ do is track directory
contents efficiently. It is intended to be the base of an efficient,
distributed source code management system. This package includes
rudimentary tools that can be used as a SCM, but you should look
elsewhere for tools for ordinary humans layered on top of this.

This is a dummy package which brings in all subpackages.

%package -n git-core
Summary:	Global Information Tracker
Group:		Development/Other
Requires:	diffutils
Requires:	rsync
Requires:	less
Requires:	openssh-clients
Suggests:	git-prompt

%description -n git-core
This is a stupid (but extremely fast) directory content manager.  It
doesn't do a whole lot, but what it _does_ do is track directory
contents efficiently. It is intended to be the base of an efficient,
distributed source code management system. This package includes
rudimentary tools that can be used as a SCM, but you should look
elsewhere for tools for ordinary humans layered on top of this.

This are the core tools with minimal dependencies.

You may want to install subversion, cpsps and/or tla to import
repositories from other VCS.

%package -n gitk
Summary:	Git revision tree visualiser
Group:		Development/Other
Requires:	git-core = %{EVRD}
Requires:	tk >= 8.4
Requires:	tcl >= 8.4

%description -n gitk
Git revision tree visualiser.

%package -n gitview
Summary:	Git graphical revision tree visualiser
Group:		Development/Other
Requires:	git-core = %{EVRD}
Requires:	python-cairo
Requires:	pygtk2.0
Requires:	python-gtksourceview

%description -n gitview
Git graphical revision tree visualiser.

%package -n %{libname}-devel
Summary:	Git development files
Group:		Development/Other
Provides:	git-devel = %{version}-%{release}

%description -n %{libname}-devel
Development files for git.

%package -n git-svn
Summary:	Git tools for importing Subversion repositories
Group:		Development/Other
Requires:	git-core = %{EVRD}, subversion
Requires:	perl-Git
Requires:	perl-SVN

%description -n git-svn
Git tools for importing Subversion repositories.

%package -n git-cvs
Summary:	Git tools for importing CVS repositories
Group:		Development/Other
Requires:	git-core = %{EVRD}
Suggests:	cvs
Suggests:	cvsps

%description -n git-cvs
Git tools for importing CVS repositories.

%package -n git-arch
Summary:	Git tools for importing Arch repositories
Group:		Development/Other
Requires:	git-core = %{EVRD}
Suggests:	tla

%description -n git-arch
Git tools for importing Arch repositories.

%package -n git-email
Summary:	Git tools for sending email
Group:		Development/Other
Requires:	git-core = %{EVRD}
Suggests:	perl-Authen-SASL
Suggests:	perl-MIME-Base64

%description -n git-email
Git tools for sending email.

%package -n perl-Git
Summary:	Perl interface to Git
Group:		Development/Perl
Requires:	git-core = %{EVRD}

%description -n perl-Git
Perl interface to Git

%package -n python-git
Summary:	Python interface to Git
Group:		Development/Python
Requires:	git-core = %{EVRD}

%description -n python-git
Python interface to Git

%package -n git-core-oldies
Summary:	Git obsolete commands, bound to extinction
Group:		Development/Other
Requires:	git-core = %{EVRD}

%description -n git-core-oldies
Git obsolete commands, bound to extinction

%package -n gitweb
Summary:	cgi-bin script for browse a git repository with web browser
Group:		System/Servers
Requires:	git-core = %{EVRD}

%description -n gitweb
cgi-bin script for browse a git repository with web browser.

%package -n git-prompt
Summary:	Shows the current git branch in your bash prompt
Group:		Shells
Requires:	git-core = %{EVRD}
Requires:	bash-completion

%description -n git-prompt
Shows the current git branch in your bash prompt.

%prep
%setup -q
# remove borring file
rm -f Documentation/.gitignore
# prefix gitweb css/png files with /gitweb
perl -pi -e 's!^(GITWEB_CSS|GITWEB_LOGO|GITWEB_FAVICON) = !$1 = /gitweb/!' Makefile
%apply_patches

%build
# same flags and prefix must be passed for make test too
%define git_make_params prefix=%{_prefix} CC=%{__cc} gitexecdir=%{_libdir}/git-core CFLAGS="%{optflags}" GITWEB_CONFIG=%{_sysconfdir}/gitweb.conf DOCBOOK_XSL_172=1
%make CC=%{__cc} AR=%{__ar} %{git_make_params} all doc gitweb/gitweb.cgi

# Produce RelNotes.txt.gz
# sed trick changes "-x.y.z.txt" to "-x.y.z.0.txt" for ordering, then undoes it
# use awk to print a newline before each RelNotes header
cd Documentation/RelNotes \
&& relnotesls="`find . -name '*.txt' | sed 's/\([0-9]\.[0-9]\.[0-9]\)\.txt/\1.0.txt/' | sort -nr | sed 's/\([0-9]\.[0-9]\.[0-9]\)\.0\.txt/\1.txt/'`" \
&& awk 'FNR == 1 { print "" } { print }' $relnotesls | gzip -9c >../RelNotes.txt.gz

%install
mkdir -p %{buildroot}%{_bindir}
%makeinstall_std CC=%{__cc} AR=%{__ar} prefix=%{_prefix} gitexecdir=%{_libdir}/git-core  CFLAGS="%{optflags}"
make install-doc CC=%{__cc} AR=%{__ar} prefix=%{_prefix} gitexecdir=%{_libdir}/git-core   DESTDIR=%{buildroot}

# Avoid dependencies on obscure perl modules
chmod -x contrib/mw-to-git/git-remote-mediawiki.perl

# (cg) Copy the whole contrib dir as docs. It contains useful scripts.
mkdir -p %{buildroot}%{_datadir}/doc/git-core
cp -ar contrib %{buildroot}%{_datadir}/doc/git-core
# (cg) Even tho' we copy the whole contrib dir, copy this rather than symlink incase the user is excluding docs
install -m 755 contrib/gitview/gitview %{buildroot}%{_bindir}

mkdir -p %{buildroot}%{_includedir}/git
cp *.h %{buildroot}%{_includedir}/git

mkdir -p %{buildroot}%{_libdir}
install -m 644 libgit.a %{buildroot}%{_libdir}/libgit.a

mv %{buildroot}/%{_prefix}/lib/perl5/site_perl %{buildroot}/%{_prefix}/lib/perl5/vendor_perl
rm -f %{buildroot}/%{perl_vendorlib}/Error.pm

mkdir -p %{buildroot}%{_datadir}/gitweb/static
install -m 755 gitweb/gitweb.cgi %{buildroot}%{_datadir}/gitweb
install -m 644 gitweb/static/*.css gitweb/static/*.png %{buildroot}%{_datadir}/gitweb/static/

mkdir -p %{buildroot}%{_sysconfdir}
install -m644 %{SOURCE2} %{buildroot}%{_sysconfdir}/gitweb.conf
# apache configuration
mkdir -p %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/gitweb.conf <<EOF
# gitweb configuration
Alias /gitweb %{_datadir}/gitweb

<Directory %{_datadir}/gitweb>
    Order allow,deny
    Allow from all
    Options ExecCgi
    DirectoryIndex gitweb.cgi
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

%find_lang %{name}

%check
# We do NO_SVN_TESTS because git's tests hardcode
# replies from svn versions older than the one
# we're shipping -- and they have changed since
LC_ALL=C %make %{git_make_params} test NO_SVN_TESTS=true

%files
# no file in the main package

%files -n git-core -f %{name}.lang
/etc/emacs/site-start.d/*
/etc/bash_completion.d/*
%{_datadir}/emacs/site-lisp/*
%{_bindir}/git
%{_bindir}/git-*
%{_libdir}/git-core
%exclude %{_libdir}/git-core/*svn*
%exclude %{_libdir}/git-core/*cvs*
%exclude %{_libdir}/git-core/git-archimport
%exclude %{_libdir}/git-core/*email*
%{_datadir}/git-core
%{_datadir}/git-gui
%{_mandir}/*/git-*
%{_mandir}/*/git.*
%{_mandir}/*/gitattributes*
%{_mandir}/*/gitignore*
%{_mandir}/*/gitmodules*
%{_mandir}/*/gitnamespaces*
%{_mandir}/*/gitcli*
%{_mandir}/*/githooks*
%{_mandir}/*/gitrepository*
%{_mandir}/*/*tutorial*
%{_mandir}/*/*glossary*
%{_mandir}/*/gitdiffcore*
%{_mandir}/*/gitworkflows*
%{_mandir}/*/gitrevisions*
%{_mandir}/*/gitcredentials*
%{_mandir}/*/gitremote-helpers*
%exclude %{_mandir}/man1/*svn*.1*
%exclude %{_mandir}/man1/*cvs*.1*
%exclude %{_mandir}/man7/*cvs*.7*
%exclude %{_mandir}/man1/*email*.1*
%exclude %{_mandir}/man1/git-archimport.1*
%doc README Documentation/*.html Documentation/howto Documentation/technical Documentation/RelNotes.txt.gz

%files -n gitk
%doc README
%{_bindir}/gitk
%{_mandir}/*/gitk*
%{_datadir}/gitk

%files -n gitview
%doc contrib/gitview/gitview.txt
%{_bindir}/gitview

%files -n %{libname}-devel
%{_includedir}/git
%{_libdir}/libgit.a

%files -n git-svn
%{_libdir}/git-core/*svn*
%{_mandir}/man1/*svn*.1*

%files -n git-cvs
%{_libdir}/git-core/*cvs*
%{_mandir}/man1/*cvs*.1*
%{_mandir}/man7/*cvs*.7*

%files -n git-arch
%{_libdir}/git-core/git-archimport
%{_mandir}/man1/git-archimport.1*

%files -n git-email
%{_libdir}/git-core/*email*
%{_mandir}/man1/*email*.1*

%files -n perl-Git
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files -n python-git
%{py_puresitedir}/*

%files -n git-core-oldies

%files -n gitweb
%doc gitweb/INSTALL gitweb/README
%config(noreplace) %{_sysconfdir}/gitweb.conf
%config(noreplace) %{_webappconfdir}/gitweb.conf
%{_datadir}/gitweb
%{_mandir}/man1/gitweb.1*
%{_mandir}/man5/gitweb.conf.5*

%files -n git-prompt
%{_sysconfdir}/profile.d/%{profile_branch}

