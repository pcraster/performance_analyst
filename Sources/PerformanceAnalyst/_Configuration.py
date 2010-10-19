versionMajor      = 0
versionMinor      = 0
versionPatchLevel = 7



def versionAsInteger():
  return versionMajor * 100 + versionMinor * 10 + versionPatchLevel

def versionAsString():
  return "{0}.{1}.{2}".format(versionMajor, versionMinor, versionPatchLevel)

def versionAsTuple():
  return (versionMajor, versionMinor, versionPatchLevel)
