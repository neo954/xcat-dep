#
#   - IO-Socket-SSL -
#   This spec file was automatically generated by cpan2rpm [ver: 2.028]
#   The following arguments were used:
#       IO-Socket-SSL-1.38.tar.gz -U --tempdir=/tmp/test
#   For more information on cpan2rpm please visit: http://perl.arix.com/
#

%define pkgname IO-Socket-SSL
%define filelist %{pkgname}-%{version}-filelist
%define NVR %{pkgname}-%{version}-%{release}
%define maketest 1

name:      perl-IO-Socket-SSL
summary:   IO-Socket-SSL - Nearly transparent SSL encapsulation for IO::Socket::INET.
version:   1.38
release:   1
vendor:    Steffen Ullrich & Peter Behroozi & Marko Asplund
packager:  Arix International <cpan2rpm@arix.com>
license:   Artistic
group:     Applications/CPAN
url:       http://www.cpan.org
buildroot: %{_tmppath}/%{name}-%{version}-%(id -u -n)
buildarch: ppc
prefix:    %(echo %{_prefix})
source:    IO-Socket-SSL-1.38.tar.gz

%description
This module is a true drop-in replacement for IO::Socket::INET that uses
SSL to encrypt data before it is transferred to a remote server or
client.	 IO::Socket::SSL supports all the extra features that one needs
to write a full-featured SSL client or server application: multiple SSL contexts,
cipher selection, certificate verification, and SSL version selection.	As an
extra bonus, it works perfectly with mod_perl.

If you have never used SSL before, you should read the appendix labelled 'Using SSL'
before attempting to use this module.

If you have used this module before, read on, as versions 0.93 and above
have several changes from the previous IO::Socket::SSL versions (especially
see the note about return values).

If you are using non-blocking sockets read on, as version 0.98 added better
support for non-blocking.

If you are trying to use it with threads see the BUGS section.

#
# This package was generated automatically with the cpan2rpm
# utility.  To get this software or for more information
# please visit: http://perl.arix.com/
#

%prep
%setup -q -n %{pkgname}-%{version} 
chmod -R u+w %{_builddir}/%{pkgname}-%{version}

%build
grep -rsl '^#!.*perl' . |
#   grep -v '.bak$' |xargs --no-run-if-empty \
grep -v '.bak$' |xargs \
%__perl -MExtUtils::MakeMaker -e 'MY->fixin(@ARGV)'
CFLAGS="$RPM_OPT_FLAGS"
%{__perl} Makefile.PL `%{__perl} -MExtUtils::MakeMaker -e ' print qq|PREFIX=%{buildroot}%{_prefix}| if \$ExtUtils::MakeMaker::VERSION =~ /5\.9[1-6]|6\.0[0-5]/ '`
%{__make} 
#%if %maketest
#%{__make} test
#%endif

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%{makeinstall} `%{__perl} -MExtUtils::MakeMaker -e ' print \$ExtUtils::MakeMaker::VERSION <= 6.05 ? qq|PREFIX=%{buildroot}%{_prefix}| : qq|DESTDIR=%{buildroot}| '`

cmd=/usr/share/spec-helper/compress_files
[ -x $cmd ] || cmd=/usr/lib/rpm/brp-compress
[ -x $cmd ] && $cmd

# SuSE Linux
#        if [ -e /etc/SuSE-release -o -e /etc/UnitedLinux-release ]
#        then
#            %{__mkdir_p} %{buildroot}/var/adm/perl-modules
#            %{__cat} `find %{buildroot} -name "perllocal.pod"`  \
#                | %{__sed} -e s+%{buildroot}++g                 \
#                > %{buildroot}/var/adm/perl-modules/%{name}
#        fi

# remove special files
find %{buildroot} -name "perllocal.pod" \
    -o -name ".packlist"                \
    -o -name "*.bs"                     \
    |xargs -i rm -f {}

# no empty directories
#        find %{buildroot}%{_prefix}             \
#            -type d -depth                      \
#            -exec rmdir {} \; 2>/dev/null

%{__perl} -MFile::Find -le '
    find({ wanted => \&wanted, no_chdir => 1}, "%{buildroot}");
    print "%doc  README.Win32 example util Changes patches docs README certs";
    for my $x (sort @dirs, @files) {
        push @ret, $x unless indirs($x);
        }
    print join "\n", sort @ret;

    sub wanted {
        return if /auto$/;

        local $_ = $File::Find::name;
        my $f = $_; s|^\Q%{buildroot}\E||;
        return unless length;
        return $files[@files] = $_ if -f $f;

        $d = $_;
        /\Q$d\E/ && return for reverse sort @INC;
        $d =~ /\Q$_\E/ && return
            for qw|/etc %_prefix/man %_prefix/bin %_prefix/share|;

        $dirs[@dirs] = $_;
        }

    sub indirs {
        my $x = shift;
        $x =~ /^\Q$_\E\// && $x ne $_ && return 1 for @dirs;
        }
    ' > %filelist

[ -z %filelist ] && {
    echo "ERROR: empty %files listing"
    exit -1
    }

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -f %filelist
%defattr(-,root,root)

%changelog
* Mon, 04 Jan 2016 gongjie@linux.vnet.ibm.com
- Rebuild on AIX 7.2
* Mon Jun 21 2010 root@c114m4h1p04.ppd.pok.ibm.com
- Initial build.
