#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (disable for bootstrap: tests need ipykernel which requires jupyter_client)

Summary:	Reference implementation of the Jupyter protocol
Summary(pl.UTF-8):	Referencyjna implementacja protokołu Jupyter
Name:		python3-jupyter_client
Version:	8.6.3
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/jupyter_client/
Source0:	https://files.pythonhosted.org/packages/source/j/jupyter_client/jupyter_client-%{version}.tar.gz
# Source0-md5:	9d57963cc1cb5623c0cc1d051e63039b
Patch0:		jupyter_client-sphinx.patch
URL:		https://pypi.org/project/jupyter_client/
BuildRequires:	python3-build
BuildRequires:	python3-hatchling >= 1.5
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.8
%if %{with tests}
BuildRequires:	python3-dateutil >= 2.8.2
%if "%{_ver_lt %{py3_ver} 3.10}" == "1"
BuildRequires:	python3-importlib_metadata >= 4.8.3
%endif
BuildRequires:	python3-ipykernel >= 6.14
BuildRequires:	python3-ipython
BuildRequires:	python3-jupyter_core >= 4.12.0
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-jupyter >= 0.4.1
#BuildRequires:	python3-pytest-asyncio
BuildRequires:	python3-pytest-timeout
BuildRequires:	python3-traitlets >= 5.3
BuildRequires:	python3-tornado >= 6.2
BuildRequires:	python3-zmq >= 23.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
#BuildRequires:	python3-ipykernel
BuildRequires:	python3-myst_parser
BuildRequires:	python3-pydata_sphinx_theme
BuildRequires:	python3-sphinx_autodoc_typehints
BuildRequires:	python3-sphinxcontrib-spelling
BuildRequires:	python3-sphinxcontrib_github_alt
BuildRequires:	python3-zmq >= 23.0
BuildRequires:	sphinx-pdg-3 >= 4
%endif
Requires:	python3-modules >= 1:3.8
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
%patch -P0 -p1

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

for f in $RPM_BUILD_ROOT%{_bindir}/jupyter-* ; do
	%{__mv} "$f" "${f}-3"
	ln -sf "$(basename ${f})-3" "$f"
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md LICENSE README.md
%attr(755,root,root) %{_bindir}/jupyter-kernel-3
%attr(755,root,root) %{_bindir}/jupyter-kernelspec-3
%attr(755,root,root) %{_bindir}/jupyter-run-3
%{_bindir}/jupyter-kernel
%{_bindir}/jupyter-kernelspec
%{_bindir}/jupyter-run
%{py3_sitescriptdir}/jupyter_client
%{py3_sitescriptdir}/jupyter_client-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_images,_static,api,*.html,*.js}
%endif
