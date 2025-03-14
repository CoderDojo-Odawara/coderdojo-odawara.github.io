import nfc

clf = nfc.ContactlessFrontend("usb")
tag = clf.connect(rdwr={'on-connect': lambda tag: False})
print(tag)
