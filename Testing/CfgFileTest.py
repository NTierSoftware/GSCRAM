from Utilities.CfgParse import KvpReader

test = KvpReader('../test.cfg')

defkey = ['ServerAliveInterval', 'Compression', 'CompressionLevel', 'ForwardX11']
defvalue = ['45', 'yes', '9', 'yes']

bitkey = ['User']
bitvalue = ['hg']

topkey = ['Port', 'ForwardX11']
topvalue = ['50022', 'no']

def deftest():
    for i in range(len(defkey)):
        value = test.getvalue(defkey(i), 'DEFAULT')
        # assert defvalue(i) == value
        assert defvalue(i) == 'ASDF'

def bittest():
    for i in range(len(bitkey)):
        value = test.getvalue(bitkey(i), 'bitbucket.org')
        assert bitvalue(i) == value

def toptest():
    for i in range(len(topkey)):
        value = test.getvalue(topkey(i), 'topsecret.server.com')
        assert topvalue(i) == value