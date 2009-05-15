Name:		speedcrunch
Version:	0.10.1
Release:	%mkrel 1
Summary:	Fast, high precision and powerful desktop calculator
License:	GPLv2+
Group:		Sciences/Mathematics
Source0:	http://speedcrunch.googlecode.com/files/%{name}-%{version}.tar.gz
URL:		http://speedcrunch.org

BuildRequires:	qt4-devel 
BuildRequires:	cmake
BuildRequires:	imagemagick
BuildRequires:	desktop-file-utils
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot


%description
SpeedCrunch is a fast, high precision and powerful desktop calculator.

Among its features are:
- high precision, up to 50 decimal digits
- to be enjoyed using keyboard
- result shown in scrollable window
- history of last expressions (use up and down arrow)
- built-in functions: abs, sqrt, pi, log, exp, ln, sin, cos, tan, sinh,
  cosh, tanh, asin, acos, atan, arsinh, arcosh, artanh
- postfix operator ! lets you compute factorials
- support for variables, e.g try x=pi/3 and then sin(x)
- special variable ans holds the last calculation result
- percent operator, try e.g. 45%*75 or price/80%
- angle mode: Alt+D for degrees, Alt+R for radians
- automatic parentheses closing, e.g. cos(pi/4 becomes cos(pi/4)

%prep
%setup -q

# fix encoding
mv LISEZMOI LISEZMOI.ISO-8859-1
iconv -f ISO-8859-1 -t UTF8 LISEZMOI.ISO-8859-1 -o LISEZMOI

%build
lrelease src/i18n/*.ts
%cmake_qt4 ../src
%make

%install
rm -rf %{buildroot}
cd build
%makeinstall DESTDIR=%{buildroot}

# move and convert speedcrunch icon
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/{16x16,32x32,48x48}/apps
pushd %{buildroot}%{_datadir}/icons/hicolor/48x48/apps
mv %{buildroot}%{_datadir}/pixmaps/%{name}.png %{name}.png
convert -resize 16x16 %{name}.png \
	%{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
convert -resize 32x32 %{name}.png \
	%{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
rm -rf %{buildroot}%{_datadir}/pixmaps
popd

# fix desktop file
sed -i -e 's/speedcrunch.png/speedcrunch/' \
	%{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-install \
	--remove-category=KDE \
	--remove-category=Utility \
	--add-category=Math \
	--add-category=X-MandrivaLinux-MoreApplications-Sciences-Mathematics \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/*

# set make_math_pngs.sh executable
chmod +x %{buildroot}%{_datadir}/%{name}/books/images/make_math_pngs.sh

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc doc/* ChangeLog ChangeLog.floatnum COPYING HACKING.txt
%doc INSTALL.txt LISEZMOI PACKAGERS README TRANSLATORS
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/%{name}
