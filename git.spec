
%define libname %mklibname git
%define profilefile 93git-branch.sh

Summary: Global Information Tracker
Name: git
Epoch: 1
Version: 1.6.3
Release: %mkrel 1
Source0: http://www.kernel.org/pub/software/scm/git/git-%{version}.tar.bz2
Source1: http://www.kernel.org/pub/software/scm/git/git-%{version}.tar.bz2.sign
Source2: gitweb.conf
Source3: %{profilefile}
License: GPLv2
Group: Development/Other
Url: http://git-scm.com/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: openssl-devel
BuildRequires: zlib-devel
BuildRequires: curl-devel
BuildRequires: expat-devel
BuildRequires: asciidoc
BuildRequires: xmlto
BuildRequires: dos2unix
BuildRequires: perl-CGI
Requires: git-core = %{epoch}:%{version}
Requires: gitk = %{epoch}:%{version}
Requires: git-svn = %{epoch}:%{version}
Suggests: git-cvs = %{epoch}:%{version}
Requires: git-email = %{epoch}:%{version}
Suggests: git-arch = %{epoch}:%{version}
Suggests: git-core-oldies = %{epoch}:%{version}
Obsoletes: linus-git < 1.5.4.3-2
Provides: linus-git

%description
This is a stupid (but extremely fast) directory content manager.  It
doesn't do a whole lot, but what it _does_ do is track directory
contents efficiently. It is intended to be the base of an efficient,
distributed source code management system. This package includes
rudimentary tools that can be used as a SCM, but you should look
elsewhere for tools for ordinary humans layered on top of this.

This is a dummy package which brings in all subpackages.


%package -n git-core
Summary: Global Information Tracker
Group: Development/Other
Requires: diffutils
Requires: rsync
Requires: less
Requires: openssh-clients
Suggests: git-prompt
Conflicts: git < 4.3.20-15
Obsoletes: gitcompletion
Provides: gitcompletion

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
Summary: Git revision tree visualiser
Group: Development/Other
Requires: git-core = %{epoch}:%{version}
Requires: tk >= 8.4
Requires: tcl >= 8.4

%description -n gitk
Git revision tree visualiser.

%package -n gitview
Summary: Git graphical revision tree visualiser
Group: Development/Other
Requires: git-core = %{epoch}:%{version}
Requires: python-cairo
Requires: pygtk2.0
Requires: python-gtksourceview

%description -n gitview
Git graphical revision tree visualiser.

%package -n %libname-devel	
Summary: Git development files	
Group: Development/Other	
Provides: git-devel = %version-%release	
 	 	
%description -n %libname-devel	
Development files for git.

%package -n git-svn
Summary:        Git tools for importing Subversion repositories
Group:          Development/Other
Requires:       git-core = %{epoch}:%{version}-%{release}, subversion
%description -n git-svn
Git tools for importing Subversion repositories.

%package -n git-cvs
Summary:        Git tools for importing CVS repositories
Group:          Development/Other
Requires:       git-core = %{epoch}:%{version}-%{release}
Suggests: 	cvs, cvsps
%description -n git-cvs
Git tools for importing CVS repositories.

%package -n git-arch
Summary:        Git tools for importing Arch repositories
Group:          Development/Other
Requires:       git-core = %{epoch}:%{version}-%{release}
Suggests:	tla
%description -n git-arch
Git tools for importing Arch repositories.

%package -n git-email
Summary:        Git tools for sending email
Group:          Development/Other
Requires:       git-core = %{epoch}:%{version}-%{release}
%description -n git-email
Git tools for sending email.

%package -n perl-Git
Summary:        Perl interface to Git
Group:          Development/Perl
Requires:       git-core = %{epoch}:%{version}-%{release}

%description -n perl-Git
Perl interface to Git

%package -n git-core-oldies
Summary:	Git obsolete commands, bound to extinction
Group:		Development/Other
Requires:	git-core = %{epoch}:%{version}-%{release}

%description -n git-core-oldies
Git obsolete commands, bound to extinction

%package -n gitweb
Summary:	cgi-bin script for browse a git repository with web browser
Group:		System/Servers
Requires:	git-core = %{epoch}:%{version}-%{release}

%description -n gitweb
cgi-bin script for browse a git repository with web browser.

%package -n git-prompt
Summary:        Shows the current git branch in your bash prompt
Group:          Shells
Requires:       git-core = %{epoch}:%{version}-%{release}
%description -n git-prompt
Shows the current git branch in your bash prompt.

%prep
%setup -q -n git-%{version}
# remove borring file
rm -f Documentation/.gitignore
# prefix gitweb css/png files with /gitweb
perl -pi -e 's!^(GITWEB_CSS|GITWEB_LOGO|GITWEB_FAVICON) = !$1 = /gitweb/!' Makefile

%build
# same flags and prefix must be passed for make test too
%define git_make_params prefix=%{_prefix} gitexecdir=%{_libdir}/git-core CFLAGS="$RPM_OPT_FLAGS" GITWEB_CONFIG=%{_sysconfdir}/gitweb.conf DOCBOOK_XSL_172=1
%make %git_make_params all doc gitweb/gitweb.cgi

# convert end of line to make rpmlint happy
dos2unix Documentation/*.html

# Produce RelNotes.txt.gz
# protect from it ever coming into existence from upstream (should be preferred)
cd Documentation
find . -name RelNotes.\* | grep -q RelNotes\\. 2>/dev/null && exit 1
# sed trick changes "-x.y.z.txt" to "-x.y.z.0.txt" for ordering, then undoes it
relnotesls="`find . -name 'RelNotes-*' | sed 's/\(-[0-9]\.[0-9]\.[0-9]\)\.txt/\1.0.txt/' | sort -nr | sed 's/\(-[0-9]\.[0-9]\.[0-9]\)\.0\.txt/\1.txt/'`"
# use awk to print a newline before each RelNotes header
awk 'FNR == 1 { print "" } { print }' $relnotesls | gzip -9c >RelNotes.txt.gz

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
%makeinstall_std prefix=%{_prefix} gitexecdir=%{_libdir}/git-core  CFLAGS="$RPM_OPT_FLAGS"
make install-doc prefix=%{_prefix} gitexecdir=%{_libdir}/git-core   DESTDIR=$RPM_BUILD_ROOT
install -m 755 contrib/gitview/gitview %buildroot%{_bindir}

mkdir -p %{buildroot}%{_includedir}/git
cp *.h %{buildroot}%{_includedir}/git

mkdir -p %{buildroot}%{_libdir}
install -m 644 libgit.a %buildroot%{_libdir}/libgit.a

mv %{buildroot}/%{_prefix}/lib/perl5/site_perl %{buildroot}/%{_prefix}/lib/perl5/vendor_perl
rm -f %{buildroot}/%{perl_vendorlib}/Error.pm

mkdir -p %{buildroot}%{_var}/www/cgi-bin/gitweb/
cp gitweb/gitweb.cgi %{buildroot}%{_var}/www/cgi-bin/
mkdir -p %{buildroot}%{_var}/www/gitweb/
cp gitweb/*.css gitweb/*.png %{buildroot}%{_var}/www/gitweb
mkdir -p %{buildroot}%{_sysconfdir}
install -m644 %{SOURCE2} %{buildroot}%{_sysconfdir}/gitweb.conf
# apache configuration
mkdir -p %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/gitweb.conf <<EOF
# gitweb configuration
Alias /gitweb %{_var}/www/gitweb

<Directory %{_var}/www/gitweb>
    Allow from all
</Directory>
EOF

# fix .sp in man files
find %{buildroot}/%{_mandir} -type f | xargs perl -e 's/\.sp$/\n\.sp/g' -pi

# emacs VC backend:
mkdir -p %{buildroot}{%_datadir/emacs/site-lisp,/etc/emacs/site-start.d}
install -m 644 contrib/emacs/*.el %{buildroot}%_datadir/emacs/site-lisp
cat >%{buildroot}/etc/emacs/site-start.d/vc_git.el <<EOF
(add-to-list 'vc-handled-backends 'GIT)
EOF

# install bash-completion file
mkdir -p  %{buildroot}%_sysconfdir/bash_completion.d
install -m644 contrib/completion/git-completion.bash %{buildroot}%_sysconfdir/bash_completion.d/

# And the prompt manipulation file
install -D -m 0644 %SOURCE3 %{buildroot}%{_sysconfdir}/profile.d/%{profilefile}

%check
LC_ALL=C %make %git_make_params test

%clean
rm -rf $RPM_BUILD_ROOT

%post -n gitweb
%{_post_webapp}

%postun -n gitweb
%{_postun_webapp}

%files
# no file in the main package

%files -n git-core
%defattr(-,root,root,0755)
/etc/emacs/site-start.d/*
/etc/bash_completion.d/*
%_datadir/emacs/site-lisp/*
%{_bindir}/git
%{_bindir}/git-*
%{_libdir}/git-core
%exclude %{_libdir}/git-core/*svn*
%exclude %{_libdir}/git-core/*cvs*
%exclude %{_libdir}/git-core/git-archimport
%exclude %{_libdir}/git-core/*email*
# %exclude %{_bindir}/git-merge-recursive-old
%{_datadir}/git-core
%{_datadir}/git-gui
# %exclude %{_datadir}/git-core/python
%{_mandir}/*/git-*
%{_mandir}/*/git.*
%{_mandir}/*/gitattributes*
%{_mandir}/*/gitignore*
%{_mandir}/*/gitmodules*
%{_mandir}/*/gitcli*
%{_mandir}/*/githooks*
%{_mandir}/*/gitrepository*
%{_mandir}/*/*tutorial*
%{_mandir}/*/*glossary*
%{_mandir}/*/gitdiffcore*
%{_mandir}/*/gitworkflows*
%exclude %{_mandir}/man1/*svn*.1*
%exclude %{_mandir}/man1/*cvs*.1*
%exclude %{_mandir}/man7/*cvs*.7*
%exclude %{_mandir}/man1/*email*.1*
%exclude %{_mandir}/man1/git-archimport.1*
%doc README Documentation/*.html Documentation/howto Documentation/technical Documentation/RelNotes.txt.gz

%files -n gitk
%defattr(-,root,root,0755)
%{_bindir}/gitk
%{_mandir}/*/gitk*
%{_datadir}/gitk
%doc README

%files -n gitview
%defattr(-,root,root,0755)
%doc contrib/gitview/gitview.txt
%{_bindir}/gitview

%files -n %{libname}-devel	
%defattr(-,root,root,0755)
%{_includedir}/git
%{_libdir}/libgit.a

%files -n git-svn
%defattr(-,root,root)
%{_libdir}/git-core/*svn*
%{_mandir}/man1/*svn*.1*
# %doc Documentation/*svn*.txt
# %doc Documentation/*svn*.html

%files -n git-cvs
%defattr(-,root,root)
%{_libdir}/git-core/*cvs*
%{_mandir}/man1/*cvs*.1*
%{_mandir}/man7/*cvs*.7*
# %doc Documentation/*git-cvs*.txt
# %doc Documentation/*git-cvs*.html

%files -n git-arch
%defattr(-,root,root)
%{_libdir}/git-core/git-archimport
%{_mandir}/man1/git-archimport.1*
# %doc Documentation/git-archimport.txt
# %doc Documentation/git-archimport.html

%files -n git-email
%defattr(-,root,root)
%{_libdir}/git-core/*email*
%{_mandir}/man1/*email*.1*
# %doc Documentation/*email*.txt
# %doc Documentation/*email*.html

%files -n perl-Git
%defattr(-,root,root)
%{perl_vendorlib}/*
%{_mandir}/man3/*
# /usr/lib/perl5/site_perl/5.8.8/Git.pm
# /usr/local/share/man/man3/Git.3pm

%files -n git-core-oldies
%defattr(-,root,root,0755)
# %{_bindir}/git-merge-recursive-old
# %{_datadir}/git-core/python

%files -n gitweb
%defattr(-,root,root,0755)
%doc gitweb/INSTALL gitweb/README
%config(noreplace) %{_sysconfdir}/gitweb.conf
%config(noreplace) %{_webappconfdir}/gitweb.conf
%{_var}/www/cgi-bin/gitweb.cgi
%{_var}/www/gitweb

%files -n git-prompt
%defattr(-,root,root,0755)
%{_sysconfdir}/profile.d/%{profilefile}
