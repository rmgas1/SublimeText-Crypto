'''
@name     Crypto
@package  sublime_plugin
@author   Derek Anderson
@requires OpenSSL

This Sublime Text 2 plugin adds AES encryption/decryption
features to the right click context menu.

Usage: Make a selection (or not), Choose AES Encrypt or AES Decrypt 
from the context menu and then enter a password

'''

import sublime, sublime_plugin, sys
from subprocess import Popen, PIPE, STDOUT

#
# Capture user input (password) and send to the CryptoCommand
#
class AesCryptCommand(sublime_plugin.WindowCommand):
  def run(self, enc):
    self.enc = enc
    message = "Create a Password:" if enc else "Enter Password:"
    self.window.show_input_panel(message, "", self.on_done, None, None)
    pass
  def on_done(self, password):
    try:
      if self.window.active_view():
        self.window.active_view().run_command("crypto", {"enc": self.enc, "password": password})
    except ValueError:
        pass


#
# Create a new output panel, insert the message and show it
#
def panel(window, message):
  p = window.get_output_panel('crypto_error')
  p_edit = p.begin_edit()
  p.insert(p_edit, p.size(), message)
  p.end_edit(p_edit)
  p.show(p.size())
  window.run_command("show_panel", {"panel": "output.crypto_error"})


#
# Encrypt/Decrypt using OpenSSL -aes128 and -base64
# EG same as running this CLI command:
#   echo "data" | openssl enc -e -aes128 -base64 -pass "pass:lolcats"
#
def crypto(view, enc_flag, password, data):
  # enc_type = '-aes-256-cbc'
  enc_type = '-aes128'
  password = "pass:%s" % password
  # Pipe our data to the stdin of `openssl`
  echo = Popen(["echo", data], stdout=PIPE)
  openssl = Popen(["openssl", "enc", enc_flag, enc_type, "-base64", "-pass", password], stdin=echo.stdout, stdout=PIPE, stderr=PIPE)
  result, error = openssl.communicate()
  # probably a wrong password was entered
  if error:
    panel(view.window(), 'Error: Wrong password?')
    return False
  # return our results without the trailing \n character
  return result[:-1]


#
# Get the selected text regions (or the whole document) and process it
#
class CryptoCommand(sublime_plugin.TextCommand, Word):
  def run(self, edit, enc, password):
    # are we encrypting or decrypting?
    enc_flag = '-e' if enc else '-d'
    # save the document size
    view_size = self.view.size()
    # get selections
    regions = self.view.sel()
    num = len(regions)
    x = len(self.view.substr(regions[0]))
    # select the whole document if there is no user selection
    if num <= 1 and x == 0:
      regions.clear()
      regions.add( sublime.Region(0, view_size) )

    # get current document encoding or set sane defaults

    encoding = self.view.encoding()
    if encoding == 'Undefined':
      encoding = 'utf-8'
    elif encoding == 'Western (Windows 1252)':
      encoding = 'windows-1252'

    # encrypt / decrypt selections
    for region in regions:
      data = self.view.substr(region)
      results = crypto(self.view, enc_flag, password, data)
      if enc:
        results = results.encode( encoding )
      else:
        results = results.decode( encoding )
      if results:
        self.view.replace(edit, region, results)