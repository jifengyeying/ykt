def fromCharCode(a, *b):
    return chr(a%65536) + ''.join([chr(i%65536) for i in b])

_keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="

def encode(a):
	t3 = ""
	i = 0
	a = _utf8_encode(a)
	while i < len(a):
		b = ord(a[i])
		i = i + 1

		try:
			c = ord(a[i])
		except IndexError:
			c = False
		i = i + 1

		try:
			d = ord(a[i])
		except IndexError:
			d = False
		i = i + 1

		e = b >> 2

		try:
			f = (b & 3) << 4 | c >> 4
		except TypeError:
			f = (b & 3) << 4

		try:
			g = (c & 15) << 2 | d >> 6
			h = d & 63
		except:
			pass


		if c == False:
			g = h = 64
		elif d == False:
			h = 64

		t3 = t3 + _keyStr[e] + _keyStr[f] + _keyStr[g] + _keyStr[h]

	return t3


def _utf8_encode(Oce12):
	Oce12 = Oce12.replace("/rn/g", "n")
	SrPH13 = ""
	for j in range(len(Oce12)):
		i = ord(Oce12[j])
		if i < 128:
			SrPH13 += fromCharCode(i)
		elif 127 < i < 2048:
			SrPH13 += fromCharCode(i >> 6 | 192)
			SrPH13 += fromCharCode(i & 63 | 128)
		else:
			SrPH13 += fromCharCode(i >> 12 | 224)
			SrPH13 += fromCharCode(i >> 6 & 63 | 128)
			SrPH13 += fromCharCode(i & 63 | 128)


	return SrPH13


def encrypt(pwd):
	key = "aW54ZWR1"
	pwd = encode(key + pwd + key)
	pwd = encode(key + pwd + key)
	pwd = encode(key + pwd + key)
	pwd = encode(key + pwd + key)
	pwd = encode(key + pwd + key)
	return pwd