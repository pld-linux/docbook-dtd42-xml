Summary:	Davenport Group DocBook DTD for technical documentation
Summary(pl):	DocBook DTD przeznaczone do pisania dokumentacji technicznej
%define rver	4.2CR2
%define ver	4.2
Name:		docbook-dtd42-xml
Version:	1.0.cr2
Release:	2
Vendor:		OASIS
License:	Free
Group:		Applications/Publishing/XML
URL:		http://www.oasis-open.org/docbook/
Source0:	http://www.oasis-open.org/docbook/xml/%{rver}/docbook-xml-%{rver}.zip
BuildRequires:	unzip
Requires(post):	/usr/bin/xmlcatalog
#Requires(post):	sgml-common >= 0.5
Requires(preun):/usr/bin/xmlcatalog
#Requires(preun):sgml-common >= 0.5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	catalog	%{_datadir}/sgml/docbook/xml-dtd-%{ver}/xmlcatalog

%description
OASIS DocBook DTD for technical documentation.

%description -l pl
DocBook DTD jest zestawem definicji dokumentów przeznaczonych do
tworzenia dokumentacji programistycznej. Stosowany jest do pisania
podrêczników systemowych, instrukcji technicznych jak i wielu innych
ciekawych rzeczy.

%prep
%setup -q -c
chmod -R a+rX *

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/sgml/docbook/xml-dtd-%{ver}

install *.{cat,dtd,mod} $RPM_BUILD_ROOT%{_datadir}/sgml/docbook/xml-dtd-%{ver}
cp -a ent $RPM_BUILD_ROOT%{_datadir}/sgml/docbook/xml-dtd-%{ver}

# instal catalog file (nfy - waiting for wiget script)
%{_bindir}/xmlcatalog --noout --add public \
	"-//OASIS//DTD DocBook XML V%{ver}//EN" \
	http://www.oasis-open.org/docbook/xml/%{ver}/docbookx.dtd \
	/etc/xml/catalog
%{_bindir}/xmlcatalog --noout --add rewriteSystem \
	http://www.oasis-open.org/docbook/xml/%{ver}/ \
	file://%{_datadir}/sgml/docbook/xml-dtd-%{ver}/ \
	/etc/xml/catalog
%{_bindir}/xmlcatalog --noout --del \
	"-//OASIS//DTD DocBook XML V%{ver}//EN" \
	/etc/xml/catalog
%{_bindir}/xmlcatalog --noout --del \
	http://www.oasis-open.org/docbook/xml/%{ver}/ \
	/etc/xml/catalog

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/bin/install-catalog --add /etc/sgml/xhtml-%{v_er}-%{version}-%{release}.cat /usr/share/sgml/html/xml-dtd-%{v_er}/xhtml.soc > /dev/null
/usr/bin/xmlcatalog --noout --add nextCatalog xhtml %{catalog} /etc/xml/catalog

%preun
/usr/bin/install-catalog --remove /etc/sgml/xhtml-%{v_er}-%{version}-%{release}.cat /usr/share/sgml/html/xml-dtd-%{v_er}/xhtml.soc > /dev/null
/usr/bin/xmlcatalog --noout --del %{catalog} /etc/xml/catalog

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%{_datadir}/sgml/docbook/*
