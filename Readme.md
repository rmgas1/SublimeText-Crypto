Crypto Sublime Text 2 Package
=============================

### Encrypt and Decrypt a document or selection(s)

This Package depends on having `openssl` installed on your system

The package will encrypt or decrypt a document or selection(s) using this command:

    echo "your selection or document" | openssl enc -e -aes128 -base64 -pass "pass:your_password"

In the future there will be a .sublime-settings file that allows you to configure the location of `openssl` and the Cipher type to use. (see Todo).


Install
-------
Installation via the [Package Control](http://wbond.net/sublime_packages/package_control) 
  
To install manually clone this project into your `Sublime Text 2\Packages` folder:

*OSX*

    git clone git://github.com/mediaupstream/SublimeText-Crypto.git ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/Crypto

*Windows*

    git clone git://github.com/mediaupstream/SublimeText-Crypto.git "%APPDATA%\Sublime Text 2\Packages\Crypto"



Usage
-----
After installation you will have:  

* Right-click menu item `Crypto` and `Tools > Crypto` with two options: 
  - `AES Encrypt`
  - `AES Decrypt`
* Default keyboard shortcuts:
  - `⌘+K,e` on OSX or `ctrl+K,e` on Linux/Windows (AES Encrypt)
  - `⌘+K,d` on OSX or `ctrl+K,d` on Linux/Windows (AES Decrypt)

The commands work on a selection, multiple selections or if nothing is selected the whole document. Once you trigger the command you will be prompted to enter a password.



Todo
----
* Test on Linux and Windows
* Create a .sublime-settings
  - Set the path to the `openssl` executable
  - Set the encryption cipher type


Author & Contributors
----------------------
[Derek Anderson](http://twitter.com/derekanderson)


License
-------
MIT License