Summary:	XML/SGML DocBook DTD 4.2
Summary(pl):	XML/SGML DocBook DTD 4.2
%define rver	4.2CR3
%define ver	4.2
Name:		docbook-dtd42-xml
Version:	1.0.cr3
Release:	2
Vendor:		OASIS
License:	Free
Group:		Applications/Publishing/XML
URL:		http://www.oasis-open.org/docbook/
Source0:	http://www.oasis-open.org/docbook/xml/%{rver}/docbook-xml-%{rver}.zip
BuildRequires:	unzip
BuildRequires:	/usr/bin/xmlcatalog
Requires(post):	/usr/bin/xmlcatalog
Requires(post):	sgml-common >= 0.5
Requires(preun):/usr/bin/xmlcatalog
Requires(preun):sgml-common >= 0.5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define dtd_path		%{_datadir}/sgml/docbook/xml-dtd-%{ver}
%define	xmlcat_file		%{dtd_path}/catalog.xml
%define	sgmlcat_file	%{dtd_path}/docbook.cat

#
# I would put following macros into /usr/lib/rpm/macros.sgml.
#
%define xmlcat_add()			/usr/bin/xmlcatalog --noout --add nextCatalog "" %1 /etc/xml/catalog
%define xmlcat_del()			/usr/bin/xmlcatalog --noout --del %1 /etc/xml/catalog
%define xmlcat_add_rewrite()	/usr/bin/xmlcatalog --noout --add rewriteSystem %1 %2 %3
%define sgmlcat_add()			/usr/bin/install-catalog --add %1 /etc/sgml/catalog > /dev/null
%define sgmlcat_del()			/usr/bin/install-catalog --remove %1 /etc/sgml/catalog > /dev/null
%define sgmlcat_fix()			echo "OVERRIDE YES" >> %1

%description
DocBook is an XML/SGML vocabulary particularly well suited to books and papers
about computer hardware and software (though it is by no means limited to only
these applications).                 

%description -l pl
DocBook DTD jest zestawem definicji dokumentów XML/SGML przeznaczonych do
tworzenia dokumentacji technicznej. Stosowany jest do pisania podrêczników
systemowych, instrukcji jak i wielu innych ciekawych rzeczy.

%prep
%setup -q -c
chmod -R a+rX *

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{dtd_path}

%sgmlcat_fix $RPM_BUILD_ROOT/%{sgmlcat_file}

install *.{cat,dtd,mod,xml} $RPM_BUILD_ROOT%{dtd_path}
cp -a ent $RPM_BUILD_ROOT%{dtd_path}

%xmlcat_add_rewrite \
	http://www.oasis-open.org/docbook/xml/%{rver} \
	file://%{dtd_path} \
	$RPM_BUILD_ROOT%{xmlcat_file}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = "1" ]; then
    %xmlcat_add %{xmlcat_file}
    %sgmlcat_add %{sgmlcat_file}
fi

%preun
if [ "$1" = "0" ]; then
    %xmlcat_del %{xmlcat_file}
    %sgmlcat_del %{sgmlcat_file}
fi

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%{dtd_path}
