#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (disable for bootstrap: tests need ipykernel which requires jupyter_client; as of 5.3.3 two test_session tests fail)

Summary:	Reference implementation of the Jupyter protocol
Summary(pl.UTF-8):	Referencyjna implementacja protokołu Jupyter
Name:		python3-jupyter_client
Version:	6.1.7
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/jupyter_client/
Source0:	https://files.pythonhosted.org/packages/source/j/jupyter_client/jupyter_client-%{version}.tar.gz
# Source0-md5:	607468e6039c3fe5566b6d2bc33ac49a
Patch0:		%{name}-mock.patch
URL:		https://pypi.org/project/jupyter_client/
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-async_generator
BuildRequires:	python3-dateutil >= 2.1
BuildRequires:	python3-ipykernel
BuildRequires:	python3-ipython
BuildRequires:	python3-jupyter_core >= 4.6.0
#BuildRequires:	python3-msgpack
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-asyncio
BuildRequires:	python3-pytest-timeout
BuildRequires:	python3-traitlets
BuildRequires:	python3-tornado >= 4.1
BuildRequires:	python3-zmq >= 13
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
#BuildRequires:	python3-ipykernel
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	python3-sphinxcontrib_github_alt
BuildRequires:	python3-zmq >= 13
BuildRequires:	sphinx-pdg-3 >= 1.3.6
%endif
Requires:	python3-modules >= 1:3.5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
jupyter_client contains the reference implementation of the Jupyter
protocol. It also provides client and kernel management APIs for
working with kernels.

%description -l pl.UTF-8
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
%patch0 -p1

%build
%py3_build %{?with_tests:test}

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

for f in $RPM_BUILD_ROOT%{_bindir}/jupyter-* ; do
	%{__mv} "$f" "${f}-3"
done

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/jupyter_client/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING.md README.md
%attr(755,root,root) %{_bindir}/jupyter-kernel-3
%attr(755,root,root) %{_bindir}/jupyter-kernelspec-3
%attr(755,root,root) %{_bindir}/jupyter-run-3
%{py3_sitescriptdir}/jupyter_client
%{py3_sitescriptdir}/jupyter_client-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_images,_static,api,*.html,*.js}
%endif
