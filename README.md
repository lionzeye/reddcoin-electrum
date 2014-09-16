Official Reddcoin Electrum Client - reference implementation
------------------------------------------------------------
* Licence: GNU GPL v3
* Author: Thomas Voegtlin
* Author: Larry Ren (laudney) forked for Reddcoin
* Language: Python
* Homepage: https://wallet.reddcoin.com

Getting Started
------------------

Create the icons

    pyrcc4 icons.qrc -o gui/qt/icons_rc.py

To install the wallet and all its dependencies, just do:

    sudo python setup.py install
    
If `setup.py` fails with "ImportError: No module named setuptools", install python-setuptools and run setup.py again

    sudo apt-get install python-setuptools
    sudo python setup.py install

Then you can run it from any directory:

    reddcoin-electrum

Or you can run it from the source code directory:

    ./reddcoin-electrum


Install in a Virtualenv (advanced)
----------------------------------

This is a more advanced setup where you install the client not to your system but only
to it's own private Python container. You can also do this as a regular user, no need
for root, except if you need to install PyQt4 to the system (see below)

Somewhere create a virtualenv and enter it

    virtualenv electrum -p python2.7
    source electrum/bin/activate

Install dependencies

    pip install --pre slowaes
    pip install ecdsa pbkdf2 requests pyasn1 pyasn1-modules qrcode tlslite numpy ltc_scrypt

PyQt4 is not available from pip and it is a PITA to build yourself anyway, install it
through your distribution and link it into the virtualenv folder. Note that the system
path of the libraries might be different on your distribution. 

On Ubuntu:
    
    sudo apt-get install python-qt4

On Gentoo:

    ln -s /usr/lib/python2.7/site-packages/sip* $VIRTUAL_ENV/lib/python2.7/site-packages/
    ln -s /usr/lib/python2.7/site-packages/PyQt4 $VIRTUAL_ENV/lib/python2.7/site-packages/

Create the icons

    pyrcc4 icons.qrc -o gui/qt/icons_rc.py

Install Reddcoin Electrum

    python setup.py install


How to Create Official Packages
------------------------------------
python mki18n.py
pyrcc4 icons.qrc -o gui/qt/icons_rc.py
python setup.py sdist --format=zip,gztar

On Mac OS X:

    # On port based installs
    sudo python setup-release.py py2app

    # On brew installs
    ARCHFLAGS="-arch i386 -arch x86_64" sudo python setup-release.py py2app --includes sip
    sudo hdiutil create -fs HFS+ -volname "Reddcoin Electrum" -srcfolder dist/Electrum.app dist/electrum-VERSION-macosx.dmg
