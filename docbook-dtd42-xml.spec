Summary:	Davenport Group DocBook DTD for technical documentation
Summary(pl):	DocBook DTD przeznaczone do pisania dokumentacji technicznej
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
%define sgmlcat_add()			/usr/bin/install-catalog --add %1 %2 > /dev/null
%define sgmlcat_del()			/usr/bin/install-catalog --remove %1 %2 > /dev/null
%define sgmlcat_fix()			echo "OVERRIDE YES" >> %1

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
install -d $RPM_BUILD_ROOT%{dtd_path}

%sgmlcat_fix $RPM_BUILD_ROOT/%{sgmlcat_file}

install *.{cat,dtd,mod,xml} $RPM_BUILD_ROOT%{dtd_path}
cp -a ent $RPM_BUILD_ROOT%{dtd_path}

# install catalog file (nfy - waiting for wiget script)
#sgmlcat2xmlcat < docbook.cat > %{xmlcat_file}
%xmlcat_add_rewrite http://www.oasis-open.org/docbook/xml/%{rver} file://%{dtd_path} $RPM_BUILD_ROOT%{xmlcat_file}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = "1" ]; then
    %sgmlcat_add %{sgmlcat_file}
    
    %xmlcat_add %{xmlcat_file}
    
fi

%preun
if [ "$1" = "0" ]; then
    %sgmlcat_del %{sgmlcat_file}
    
    %xmlcat_del %{xmlcat_file}

fi

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%{dtd_path}
