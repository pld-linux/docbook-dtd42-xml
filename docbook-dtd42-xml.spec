
#
# todo:
# - use XML ISO entities from sgml-common
#

Summary:	XML/SGML DocBook DTD 4.2
Summary(pl):	XML/SGML DocBook DTD 4.2
%define ver	4.2
Name:		docbook-dtd42-xml
Version:	1.0
Release:	1
Vendor:		OASIS
License:	Free
Group:		Applications/Publishing/XML
URL:		http://www.oasis-open.org/docbook/
Source0:	http://www.oasis-open.org/docbook/xml/%{ver}/docbook-xml-%{ver}.zip
BuildRequires:  unzip
Requires(post,preun):   /usr/bin/xmlcatalog
Requires:   libxml2-progs >= 2.4.17-6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define dtd_path		%{_datadir}/sgml/docbook/xml-dtd-%{ver}
%define	xmlcat_file		%{dtd_path}/catalog.xml
%define	sgmlcat_file	%{dtd_path}/catalog

#
# I would put following macros into /usr/lib/rpm/macros.sgml.
#
%define xmlcat_add()			/usr/bin/xmlcatalog --noout --add nextCatalog "" %1 /etc/xml/catalog
%define xmlcat_del()			/usr/bin/xmlcatalog --noout --del %1 /etc/xml/catalog
%define xmlcat_add_rewrite	    /usr/bin/xmlcatalog --noout --add rewriteSystem 
%define sgmlcat_add()			/usr/bin/install-catalog --add %1 %2 > /dev/null
%define sgmlcat_del()			/usr/bin/install-catalog --remove %1 %2 > /dev/null

%define sgmlcat_fix()			cat << EOF >> %1
OVERRIDE YES
  -- default decl --
SGMLDECL "../../xml.dcl"
  -- hacks for opensp --
SYSTEM "file://%{_datadir}/sgml/docbook/xml-dtd-%{ver}/docbookx.dtd" "%{dtd_path}/docbookx.dtd"
SYSTEM "http://www.oasis-open.org/docbook/xml/%{ver}/docbookx.dtd"   "%{dtd_path}/docbookx.dtd"

EOF

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

install *.{xml,dtd,mod} $RPM_BUILD_ROOT%{dtd_path}
cp -a ent $RPM_BUILD_ROOT%{dtd_path}

%sgmlcat_fix $RPM_BUILD_ROOT%{sgmlcat_file}
grep -v 'ISO ' docbook.cat >> $RPM_BUILD_ROOT%{sgmlcat_file}

%xmlcat_add_rewrite \
	http://www.oasis-open.org/docbook/xml/%{ver} \
	file://%{dtd_path} \
	$RPM_BUILD_ROOT%{xmlcat_file}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if ! grep -q /etc/sgml/xml-docbook-%{ver}.cat /etc/sgml/catalog ; then
    sgmlcat_add /etc/sgml/xml-docbook-%{ver}.cat %{sgmlcat_del}
fi
if ! grep -q %{dtdpath}/catalog.xml /etc/xml/catalog ; then
    xmlcat_add %{dtdpath}/catalog.xml
fi

%preun
if [ "$1" = "0" ] ; then
    sgmlcat_del /etc/sgml/xml-docbook-%{ver}.cat %{sgmlcat_file}
    xmlcat_del %{dtdpath}/catalog.xml
fi

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%{dtd_path}
