%{?_javapackages_macros:%_javapackages_macros}
Name:           apache-rat
Version:        0.10
Release:        6.1
Summary:        Apache Release Audit Tool (RAT)

Group:          Development/Java
License:        ASL 2.0
URL:            http://creadur.apache.org/rat/
Source0:        http://www.apache.org/dist/creadur/%{name}-%{version}/%{name}-%{version}-src.tar.bz2
Patch2:         apache-rat-0.8-test.patch
Patch3:         0001-Update-to-Maven-Doxia-1.6.patch
BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(commons-cli:commons-cli)
BuildRequires:  mvn(commons-collections:commons-collections)
BuildRequires:  mvn(commons-io:commons-io)
BuildRequires:  mvn(commons-lang:commons-lang)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.ant:ant)
BuildRequires:  mvn(org.apache.ant:ant-antunit)
BuildRequires:  mvn(org.apache.ant:ant-testutil)
BuildRequires:  mvn(org.apache:apache:pom:)
BuildRequires:  mvn(org.apache.commons:commons-compress)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-core)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-decoration-model)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-sink-api)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-site-renderer)
BuildRequires:  mvn(org.apache.maven:maven-artifact)
BuildRequires:  mvn(org.apache.maven:maven-artifact-manager)
BuildRequires:  mvn(org.apache.maven:maven-model)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.apache.maven:maven-project)
BuildRequires:  mvn(org.apache.maven:maven-settings)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-dependency-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-invoker-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.reporting:maven-reporting-api)
BuildRequires:  mvn(org.apache.maven.shared:maven-plugin-testing-harness)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)

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

%description core
The core functionality of RAT, shared by the Ant tasks, and the Maven plugin.
It also includes a wrapper script "apache-rat" that should be the equivalent
to running upstream's "java -jar apache-rat.jar".


%package plugin
Summary:        Maven plugin for %{name}

%description plugin
Maven plugin for running RAT, the Release Audit Tool.


%package tasks
Summary:        Ant tasks for %{name}

%description tasks
Ant tasks for running RAT.


%package javadoc
Summary:        Javadocs for %{name}

%description javadoc
This package contains the API documentation for %{name}.


%prep
%setup -q -n %{name}-%{version}
%patch2 -p1 -b .test
%patch3 -p1

# apache-rat is a module bundling other RAT modules together and as
# such it is not needed.
%pom_disable_module apache-rat

# maven-antrun-plugin is used for running tests only and tests are
# skipped anyways.  See rhbz#988561
%pom_remove_plugin :maven-antrun-plugin apache-rat-tasks

# wagon-ssh is not needed in Fedora.
%pom_xpath_remove pom:extensions

%build
# Tests are skipped because of incompatibility with Maven 3
%mvn_build -s -f -X

%install
%mvn_install

#Wrapper script
%jpackage_script org.apache.rat.Report "" "" %{name}/%{name}-core:commons-cli:commons-io:commons-collections:commons-compress:commons-lang:junit apache-rat true 

#Ant taksks
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ant.d
echo "apache-rat/rat-core apache-rat/rat-tasks" > $RPM_BUILD_ROOT%{_sysconfdir}/ant.d/%{name}


%files -f .mfiles-%{name}-project
%doc LICENSE NOTICE

%files core -f .mfiles-%{name}-core
%doc README.txt RELEASE_NOTES.txt
%doc LICENSE NOTICE
%dir %{_javadir}/%{name}
%{_bindir}/%{name}

%files plugin -f .mfiles-%{name}-plugin

%files tasks -f .mfiles-%{name}-tasks
%{_sysconfdir}/ant.d/%{name}

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE


%changelog
* Mon Aug 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.10-6
- Update to Maven Doxia 1.6

* Fri Jun 13 2014 Michal Srb <msrb@redhat.com> - 0.10-5
- Fix FTBFS (Resolves: #1105955)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.10-3
- Remove wagon-ssh extension from POM

* Thu Oct  3 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.10-2
- Add missing BR
- Update to current packaging guidelines

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

