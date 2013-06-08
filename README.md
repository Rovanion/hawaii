Hawaii Continuous Integration
=============================

Master repository for the Hawaii desktop environment.
It contains git submodules for the whole desktop environment, something
very useful for continuous integration that also make building from git
easier.

[![Build Status](https://secure.travis-ci.org/hawaii-desktop/hawaii.png)](http://travis-ci.org/hawaii-desktop/hawaii)

Travis CI runs on Ubuntu 12.04 which doesn't have updated Qt 5 packages, therefore the build
fails and continuous integration has been disabled.

Introduction
------------

The first time you check *hawaii* out you will notice that submodules
are empty folders.  This is because the master repository is uninitialized.

Remembmer that the master repository don't include the latest version of the
submodules, just a pointer to the latest known working revision for each of them.

More information in the next chapters.

Read more about git submodules [here](http://git-scm.com/book/en/Git-Tools-Submodules).

### A note on the build process

Building a module is a four step process:

 1. Run cmake to configure the submodule.
 2. Run make to compile the software.
 3. Run sudo make install to install the software.
 4. Create a cookie that indicates the submodule was already built.

If you see a password prompt it's probably the installation step that
is asking the password.  This might happen multiple times during the
build process if the build time is greater than sudo timeout.

Dependencies
------------

Every submodule needs CMake 2.8.11+ and Qt 5 installed.

Some submodules have more requirements:

* The **greenisland** submodule requires both Wayland and qtwayland.
If you don't want to build **greenisland** just disable
it with the --blacklist argument (see the *"Blacklist and whitelist"*
chapter).
* The **login-manager** submodule requires systemd which is not
available on every GNU/Linux distribution out there.
If you don't want to build **login-manager** just disable
it with the --blacklist argument (see the *"Blacklist and whitelist"*
chapter).

Also the AccountsService DBus service must be installed to make
user management working.  The following submodules require
AccountsService at runtime:

* **greenisland**
* **login-manager**
* **system-preferences**

If you are building under Maui there's no problem because it satisfies
Hawaii requirements, but you might not be so lucky with other distributions.

ArchLinux is also a reccomended distribution.

### Build external dependencies from sources

If your system doesn't provide a recent CMake version take a look at [here](http://www.cmake.org/cmake/resources/software.html),
download CMake sources, build and install it.

Read the following pages to build Qt 5 and Wayland from sources:

* http://wayland.freedesktop.org/building.html
* http://qt-project.org/wiki/Building_Qt_5_from_Git

### Install dependencies on ArchLinux

An ArchLinux repository for x86_64 have been made.
It contains both external dependencies (Wayland, libxkbcommon, Mesa, Qt5, ...)
and the Hawaii desktop environment.

If you are going to build Hawaii from git using the tools provided by this
repository you would only install the external dependencies.

For starters, add the following to your /etc/pacman.conf:

```
[hawaii]
Server = http://archive.maui-project.org/archlinux/$repo/os/$arch
SigLevel = TrustAll
```

Now install all the external dependencies:

```sh
pacman -Syu qt5-qtbase-for-hawaii-git qt5-qtwayland-git qt5-qtsvg-git qt5-qtimageformats-git qt5-qtmultimedia-git qt5-qttools-git qt5-qt3d-git qt5-qtgraphicaleffects-git
```

If you want to develop with QtCreator you will also need to install its package:

```sh
pacman -Syu qtcreator-for-qt5-git
```

These packages install:

 * Wayland, Mesa and libxkbcommon in /usr
 * Qt5 in /opt/qt5

As you can see, Qt5 is installed in a non standard location to avoid to interfere with your existing
installation.

Add it to your path before building Hawaii:

```sh
export PATH=/opt/qt5/bin:$PATH
```

Arch Linux users also need to add /opt/qt5/lib to LD_LIBRARY_PATH during the post-installation phase.
See the [Post-installation](#post-installation) section.

How to use it
-------------

### Fetch submodules

The first time you use this module you have to fetch all the submodules.
Type the following command in order to fetch the submodules:

```sh
./init-repository fetch
```

To see more information about fetch arguments:

```sh
./init-repository fetch -h
```

### Change GitHub repositories URL

You can switch between http and ssh for all the GitHub repositories.
This is only useful for developers, in fact they usually prefer working with
ssh because it doesn't ask for passwords when pushing the changes (it uses
the ssh key).

Switch to http typing this:

```sh
./init-repository switch --http
```

And switch to ssh with this command:

```sh
./init-repository switch --ssh
```

### Update submodules

Just pull a new version of the master repository to get updates to both
the init-repository and compile scripts and submodules:

```sh
git pull
git submodule update
```

### Forward submodules

Every time you want to pull a new version of the submodules instead of using
the one provided by the master repository make sure each submodule has the
appropriate branch selected and do:

```sh
./init-repository forward
```

To see more information about forward arguments:

```sh
./init-repository forward -h
```

Submodules that gets updated running this command will be rebuilt the next
time you run the compile script.

However most of you guys won't need to do this.

### Build the submodules

The following command builds the software with default parameters, this means
that the build type is RelWithDebInfo (release mode with debugging information)
and everything gets installed under the Maui file hierarchy.

```sh
./compile
```

To see more information about compile arguments:

```sh
./compile -h
```

You can change the build profile With the --build-type argument, available
profiles are:

* **Release**: produce fully optimized code without debugging symbols.
* **Debug**: executables are not optimized and contains debugging
  symbols.
* **RelWithDebInfo** (default): same as the **Release** mode with
  debugging symbols.

Build time can be reduced if you have a multi-core or multi-processor system
using the --jobs argument:

```sh
./compile --jobs 5
```

Usually it's better not to exceed NCORES + 1 with the --jobs argument.

Remember that once submodules are built they won't be rebuilt automatically
by subsequent launches of compile.  To force a rebuild run compile like this:

```sh
./compile --rebuild
```

You can also build only specific submodules and their dependencies, for example
the following command will build vibe and its dependencies (kde-extra-cmake-modules and solid):

```sh
./compile --module vibe
```

### Post-installation

Once you are done building remember to properly configure your environment:

```sh
# Save original environment variables
export OLD_PATH=$PATH
export OLD_QT_MESSAGE_PATTERN=$QT_MESSAGE_PATTERN
export OLD_QT_PLUGIN_PATH=$QT_PLUGIN_PATH
export OLD_QML2_IMPORT_PATH=$QML2_IMPORT_PATH
export OLD_XDG_DATA_DIRS=$XDG_DATA_DIRS
export OLD_LD_LIBRARY_PATH=$LD_LIBRARY_PATH
export OLD_DESKTOP_SESSION=$DESKTOP_SESSION

# Change environment variables for Hawaii
baselibdir=/opt/hawaii/lib
libdir=$baselibdir
[ "$(uname -m)" = "x86_64" ] && libdir=$libdir:${baselibdir}64
if [ -f /etc/debian_version ]; then
  DEB_HOST_MULTIARCH=$(dpkg-architecture -qDEB_HOST_MULTIARCH)
  libdir=$libdir:${baselibdir}/$DEB_HOST_MULTIARCH
fi

export PATH=/opt/hawaii/bin:$PATH
export QT_MESSAGE_PATTERN='%{appname}(%{pid})/%{category} %{function}: %{message}'
export QT_PLUGIN_PATH=/opt/hawaii/plugins:$QT_PLUGIN_PATH
export QML2_IMPORT_PATH=/opt/hawaii/qml:$QML2_IMPORT_PATH
export XDG_DATA_DIRS=$XDG_DATA_DIRS:/opt/hawaii/share/
export LD_LIBRARY_PATH=$libdir:$LD_LIBRARY_PATH
export DESKTOP_SESSION=hawaii
```

Installing all the software under /opt/hawaii has the advantage that in order
to uninstall you can just remove the whole directory, but you can install in
whatever path you want, even /usr/local.

You might not want to set the environment variables above permanently, you can
put them into a separate file and load it when you want to use Hawaii and
its applications.

Copy the code above, paste it into ~/hawaiienv and then write a ~/hawaiiunenv
with the following code:

```sh
export PATH=$OLD_PATH
export QT_MESSAGE_PATTERN=$OLD_QT_MESSAGE_PATTERN
export QT_PLUGIN_PATH=$OLD_QT_PLUGIN_PATH
export QML2_IMPORT_PATH=$OLD_QML2_IMPORT_PATH
export XDG_DATA_DIRS=$OLD_XDG_DATA_DIRS
export LD_LIBRARY_PATH=$OLD_LD_LIBRARY
export DESKTOP_SESSION=$OLD_DESKTOP_SESSION
```

When you want to use Hawaii and its applications just do:

```sh
source ~/hawaiienv
```

When you want to restore the environment variables to their original state:

```sh
source ~/hawaiiunenv
```

**NOTE:** Remember that the above instructions only take into account Hawaii
and assume that all the external dependencies were previously installed
into the standard locations.

If you have installed any of the external dependencies (such as CMake, Mesa,
Wayland or Qt5) in a non-standard location you have to change the above
instruction accordingly.

A note for developers
---------------------

The init_repository script fetches all submodules to a known good revision,
which might be behind the master branch.

Developers need to checkout the master branch before making any changes.

This is done by typing a simple git command, for the sake of this example
we assume you want to make contributions to the *greenisland* submodule:

```sh
cd greenisland
git checkout master
```

If you have commit access you might want to switch the origin URLs to
ssh:

```sh
./init_repository switch --ssh
```

See "Change GitHub repositories URL" for more information.

Blacklist and whitelist
-----------------------

The compile script also lets you specify a blacklist and a whitelist
of submodules.

In the following example we assume that compile ignores icon-themes by
default. We put kde-solid and vibe into the blacklist and override the
default blacklist by placing icon-themes on the whitelist:

```sh
./compile --blacklist kde-solid vibe --whitelist icon-themes
```

If both --blacklist and --whitelist are passed, the latter takes
precedence.

*Beware*, if you blacklist a submodule that is a dependency of another
submodule the build might break.  There's no control, you have to be clever.
