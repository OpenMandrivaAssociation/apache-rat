%_javapackages_macros
Name:           apache-rat
Version:        0.10
Release:        1.0%{?dist}
Summary:        Apache Release Audit Tool (RAT)


License:        ASL 2.0
URL:            http://creadur.apache.org/rat/
Source0:        http://www.apache.org/dist/creadur/%{name}-%{version}/%{name}-%{version}-src.tar.bz2
Patch2:         apache-rat-0.8-test.patch
BuildArch:      noarch

BuildRequires:  jpackage-utils
BuildRequires:  java-devel
BuildRequires:  maven-local
BuildRequires:  maven-antrun-plugin
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-dependency-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-invoker-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-plugin-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-site-plugin
BuildRequires:  maven-source-plugin
BuildRequires:  maven-surefire-maven-plugin
BuildRequires:  maven-wagon

BuildRequires:  ant-antunit
BuildRequires:  ant-testutil
BuildRequires:  apache-commons-compress

Requires:       jpackage-utils
Requires:       java

%description
Release Audit Tool (RAT) is a tool to improve accuracy and efficiency when
checking releases. It is heuristic in nature: making guesses about possible
problems. It will produce false positives and cannot find every possible
issue with a release. It's reports require interpretation.

RAT was developed in response to a need felt in the Apache Incubator to be
able to review releases for the most common faults less labor intensively.
It is therefore highly tuned to the Apache style of releases.

This package just contains meta-data, you will want either apache-rat-tasks,
or apache-rat-plugin.


%package core
Summary:        Core functionality for %{name}

Requires:       %{name} = %{version}-%{release}
Requires:       apache-commons-cli
Requires:       apache-commons-collections
Requires:       apache-commons-compress
Requires:       apache-commons-lang
Requires:       apache-commons-io
Requires:       junit

%description core
The core functionality of RAT, shared by the Ant tasks, and the Maven plugin.
It also includes a wrapper script "apache-rat" that should be the equivalent
to running upstream's "java -jar apache-rat.jar".


%package plugin
Summary:        Maven plugin for %{name}

Requires:       %{name}-core = %{version}-%{release}

%description plugin
Maven plugin for running RAT, the Release Audit Tool.


%package tasks
Summary:        Ant tasks for %{name}

Requires:       %{name}-core = %{version}-%{release}

%description tasks
Ant tasks for running RAT.


%package javadoc
Summary:        Javadocs for %{name}

Requires:       jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.


%prep
%setup -q -n %{name}-%{version}
%patch2 -p1 -b .test


%build
mvn-rpmbuild -DskipTests=true package javadoc:aggregate

%install
#Dirs
mkdir -p $RPM_BUILD_ROOT%{_javadir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_mavenpomdir}

#Parent pom
cp -p pom.xml \
  $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-%{name}.pom
%add_maven_depmap JPP.%{name}-%{name}.pom

#Components
for comp in core plugin tasks
do
  jarname=%{name}-${comp}
  jarfile=$jarname/target/${jarname}-%{version}.jar
  cp -p $jarfile $RPM_BUILD_ROOT%{_javadir}/%{name}/${jarname}.jar
  cp -p ${jarname}/pom.xml \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-${jarname}.pom
  %add_maven_depmap JPP.%{name}-${jarname}.pom %{name}/${jarname}.jar -f ${comp}
done

#Wrapper script
%jpackage_script org.apache.rat.Report "" "" %{name}/%{name}-core:commons-cli:commons-io:commons-collections:commons-compress:commons-lang:junit apache-rat true 

#Ant taksks
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ant.d
echo "apache-rat/rat-core apache-rat/rat-tasks" > $RPM_BUILD_ROOT%{_sysconfdir}/ant.d/%{name}

#Javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/
cp -rp target/site/apidocs \
   $RPM_BUILD_ROOT%{_javadocdir}/%{name}


%files
%doc LICENSE NOTICE README.txt RELEASE_NOTES.txt
%{_mavenpomdir}/JPP.%{name}-%{name}.pom
%{_mavendepmapfragdir}/%{name}
%dir %{_javadir}/%{name}

%files core
%doc LICENSE NOTICE
%{_mavenpomdir}/JPP.%{name}-%{name}-core.pom
%{_mavendepmapfragdir}/%{name}-core
%{_bindir}/%{name}
%{_javadir}/%{name}/%{name}-core.jar

%files plugin
%doc LICENSE NOTICE
%{_mavenpomdir}/JPP.%{name}-%{name}-plugin.pom
%{_mavendepmapfragdir}/%{name}-plugin
%{_javadir}/%{name}/%{name}-plugin.jar

%files tasks
%doc LICENSE NOTICE
%{_sysconfdir}/ant.d/%{name}
%{_mavenpomdir}/JPP.%{name}-%{name}-tasks.pom
%{_mavendepmapfragdir}/%{name}-tasks
%{_javadir}/%{name}/%{name}-tasks.jar

%files javadoc
%doc LICENSE NOTICE
%{_javadocdir}/%{name}


%changelog
* Tue Sep 3 2013 Orion Poplawski <orion@cora.nwra.com> 0.10-1
- Update to 0.10

* Fri Aug 9 2013 Orion Poplawski <orion@cora.nwra.com> 0.9-1
- Update to 0.9

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 11 2013 Orion Poplawski <orion@cora.nwra.com> 0.8-10
- Split up depmap fragments (bug 973242)

* Tue Feb 26 2013 Orion Poplawski <orion@cora.nwra.com> 0.8-9
- Drop BR on maven-doxia and maven-doxia-sitetools (bug #915606)

* Tue Feb 12 2013 Orion Poplawski <orion@cora.nwra.com> 0.8-8
- Add apache-rat wrapper script to apache-rat-core (bug #907782)
- Disable tests for now due to Fedora maven bug

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0.8-7
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Aug 16 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.8-6
- Run mvn-rpmbuild package instead of install

* Thu Aug 16 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.8-5
- Install NOTICE files
- Remove defattr

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 7 2011 Orion Poplawski <orion@cora.nwra.com> 0.8-2
- Update to maven 3

* Tue Dec 6 2011 Orion Poplawski <orion@cora.nwra.com> 0.8-1
- Update to 0.8 release
- Add BR maven-invoker-plugin

* Thu Apr 28 2011 Orion Poplawski <orion@cora.nwra.com> 0.8-0.7.20100827
- Add needed requires to core

* Thu Mar 3 2011 Orion Poplawski <orion@cora.nwra.com> 0.8-0.6.20100827
- Drop unneeded rm from %%install
- Don't ship BUILD.txt
- Cleanup Requires

* Mon Dec 27 2010 Orion Poplawski <orion@cora.nwra.com> 0.8-0.5.20100827
- Drop maven settings patch
- Add svn revision to export command
- Set maven.test.failure.ignore=true instead of maven.test.skip
- Use %%{_mavenpomdir}

* Thu Dec 9 2010 Orion Poplawski <orion@cora.nwra.com> 0.8-0.4.20100827
- Change BR to ant-antunit
- Drop versioned jar and javadoc
- Drop BuildRoot and %%clean

* Mon Nov 1 2010 Orion Poplawski <orion@cora.nwra.com> 0.8-0.3.20100827
- Add /etc/ant.d/apache-rat

* Fri Oct 29 2010 Orion Poplawski <orion@cora.nwra.com> 0.8-0.2.20100827
- First real working package

* Wed Aug 11 2010 Orion Poplawski <orion@cora.nwra.com> 0.8-0.1
- Initial Fedora package
