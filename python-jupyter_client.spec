#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (disable for bootstrap: tests need ipykernel which requires jupyter_client; as of 5.3.3 two test_session tests fail)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Reference implementation of the Jupyter protocol
Summary(pl.UTF-8):	Referencyjna implementacja protokołu Jupyter
Name:		python-jupyter_client
Version:	5.3.3
Release:	4
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/jupyter_client/
Source0:	https://files.pythonhosted.org/packages/source/j/jupyter_client/jupyter_client-%{version}.tar.gz
# Source0-md5:	dd4f60f3ccf41cd54b0c3719a6610a1a
URL:		https://pypi.org/project/jupyter_client/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-dateutil >= 2.1
BuildRequires:	python-ipykernel
BuildRequires:	python-ipython
BuildRequires:	python-jupyter_core
BuildRequires:	python-mock
BuildRequires:	python-pytest
BuildRequires:	python-traitlets
BuildRequires:	python-tornado >= 4.1
BuildRequires:	python-zmq >= 2.1
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-dateutil >= 2.1
BuildRequires:	python3-ipykernel
BuildRequires:	python3-ipython
BuildRequires:	python3-jupyter_core
BuildRequires:	python3-pytest
BuildRequires:	python3-traitlets
BuildRequires:	python3-tornado >= 4.1
BuildRequires:	python3-zmq >= 2.1
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
#BuildRequires:	python3-ipykernel
BuildRequires:	python3-sphinxcontrib_github_alt
BuildRequires:	python3-zmq >= 2.1
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
jupyter_client contains the reference implementation of the Jupyter
protocol. It also provides client and kernel management APIs for
working with kernels.

%description -l pl.UTF-8
jupyter_client zawiera referencyjną implementację protokołu Jupyter.
Zawiera także API klienckie i zarządzania jądrami.

%package -n python3-jupyter_client
Summary:	Reference implementation of the Jupyter protocol
Summary(pl.UTF-8):	Referencyjna implementacja protokołu Jupyter
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-jupyter_client
jupyter_client contains the reference implementation of the Jupyter
protocol. It also provides client and kernel management APIs for
working with kernels.

%description -n python3-jupyter_client -l pl.UTF-8
jupyter_client zawiera referencyjną implementację protokołu Jupyter.
Zawiera także API klienckie i zarządzania jądrami.

%package apidocs
Summary:	API documentation for Python jupyter_client module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona jupyter_client
Group:		Documentation

%description apidocs
API documentation for Python jupyter_client module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona jupyter_client.

%prep
%setup -q -n jupyter_client-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

for f in $RPM_BUILD_ROOT%{_bindir}/jupyter-* ; do
	%{__mv} "$f" "${f}-2"
done

%py_postclean
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/jupyter_client/tests
%endif

%if %{with python3}
%py3_install

for f in $RPM_BUILD_ROOT%{_bindir}/jupyter-*[!2] ; do
	%{__mv} "$f" "${f}-3"
done

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/jupyter_client/tests
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc COPYING.md README.md
%attr(755,root,root) %{_bindir}/jupyter-kernel-2
%attr(755,root,root) %{_bindir}/jupyter-kernelspec-2
%attr(755,root,root) %{_bindir}/jupyter-run-2
%{py_sitescriptdir}/jupyter_client
%{py_sitescriptdir}/jupyter_client-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-jupyter_client
%defattr(644,root,root,755)
%doc COPYING.md README.md
%attr(755,root,root) %{_bindir}/jupyter-kernel-3
%attr(755,root,root) %{_bindir}/jupyter-kernelspec-3
%attr(755,root,root) %{_bindir}/jupyter-run-3
%{py3_sitescriptdir}/jupyter_client
%{py3_sitescriptdir}/jupyter_client-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_images,_static,api,*.html,*.js}
%endif
