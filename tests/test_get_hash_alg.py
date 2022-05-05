from hash import get_hash_alg


def test_get_hash_alg_md5():
    assert get_hash_alg("main.py", "md5") == "a12382dd04e3c6576de6b9734abef210  main.py"


def test_get_hash_alg_sha512():
    assert get_hash_alg("main.py",
                        "sha512") == "be2ddcf46bfdbeb1ca9050248e34d887d7c5d0d44b6237d1b1667d1c00dd16b9c95bf7276ca44ba698f4429eb53385af4646e1f8f5b790418237dca56765c2fb  main.py"


def test_get_hash_alg_sha384():
    assert get_hash_alg("main.py",
                        "sha384") == "aa9bc1985b6f4685f9fc0c6ec554243253b6784e1ddab43a7d952090f7962a38e022aff9dd6c483905845b0eda466ff8  main.py"


def test_get_hash_alg():
    assert get_hash_alg("main.py",
                        "sha256") == "e979bab5b5ce7d34e3c0cdb45812547654ce71248d3b8acade62846d50c9c3b0  main.py"


def test_get_hash_alg_blake2s():
    assert get_hash_alg("main.py",
                        "blake2s") == "2ca7b0bc1d5e1f70ec72c3c7533f744aaf0aadcc19b182f03920a0c2a2def8cc  main.py"


def test_get_hash_alg_sha3_512():
    assert get_hash_alg("main.py",
                        "sha3_512") == "fc652b251031d7eb3c9f5e6ce10003f8d456b0f86d3782506f08a0dd8265977a782b5be6737df5e8b6c731805a442ed314b399914a5d25569c75ac0158426093  main.py"


def test_get_hash_alg_sha3_384():
    assert get_hash_alg("main.py",
                        "sha3_384") == "8685885f86fe234e9916559f99ac3dfb484aff647c06010564a9fb567b36c72ec9acc2bcd2f24cd7e7440b47d5459bde  main.py"


def test_get_hash_alg_shake_256():
    assert get_hash_alg("main.py",
                        "shake_256") == "9f73431ba730817684867069bd52597a75d12ce6c44abfc1243877d33b5f0fd4e866273f74e56fe9998ed9d681c36d71f33079646df7082e352724b77c2d209e6c65b201558e3b86acb7bdfd021bd1f9b9873a1986efb53a077d3de00cec123de3fc76ff0c3e67e4a108749c60acbc541059b3a73d2ec312754f88b0a7433a7f048e14398d9df683e8b4db530d48dc2a336625fa4f159db13d2e28a441d01737eee839ca26d759c2c072678b9ff5cea556294f5598afe94667cbb8ca8f6e72c320bda182dd68f3a6a122436410a56e32cdce9285528c508f01aa054ac4949758b57c9d11f847b3542faf78beba327a144e4dc3c3f521ef252192b268bfaef7  main.py"


def test_get_hash_alg_sha224():
    assert get_hash_alg("main.py", "sha224") == "79b76356d44402183785107ef7b294962d56f38bfe48443e18b445ab  main.py"


def test_get_hash_alg_shake_128():
    assert get_hash_alg("main.py",
                        "shake_128") == "91495af179cf9fca1e77d2fc512083f27d6a0647227650fed0df6295d1863bc93c64c2e06e005c562fb66df225655f92f35162c9e9b799071db53049da60a25bfdea0382e57d7b6e4ec972cdef154ec0b999023a73942b65b298a313506d69a5b23467841a360ead9aee90965acefc4bf41f1620e742f6a8f990ecb42e87edbcaa823f140723149c506558e5dd6ba3265eeed740f73bdc5b4716eeb0699d7403ab3299ecd4e75f52d751faa9210857bb92affca58955b5c50d2ee8e0c71a32462b397e0d6df7a00bd4b7fbf4ba71031c9b60c9c45a0ac59902729fdcfdb5089db63b0ce66be72e4dec5f88aa02a30f1de9567b3ae76c480bee6edbe96f3e02  main.py"


def test_get_hash_alg_sha3_224():
    assert get_hash_alg("main.py", "sha3_224") == "2d054f5f64cbb6419d50dc82be049595cf3aa27279c30b1547f59d10  main.py"


def test_get_hash_alg_sha1():
    assert get_hash_alg("main.py", "sha1") == "01300550040e197e2c936d41b56a4fd50fb0fdc3  main.py"


def test_get_hash_alg_sha384():
    assert get_hash_alg("main.py",
                        "sha384") == "aa9bc1985b6f4685f9fc0c6ec554243253b6784e1ddab43a7d952090f7962a38e022aff9dd6c483905845b0eda466ff8  main.py"


def test_get_hash_alg_blake2b():
    assert get_hash_alg("main.py",
                        "blake2b") == "74483c4becd5a9e6fd0018a8ab756ebad60b4448bd6cff720c79a91e5b523e07e8d9479a080eddefc1e65f04eb432fdc8d414955400ac41967494a96d7bb49c0  main.py"


def test_get_hash_alg_sha3_256():
    assert get_hash_alg("main.py",
                        "sha3_256") == "d3813c7eb2b571ece44d842b88c8e77e7a30125f74a966d170e6a581a245fca3  main.py"


def test_get_hash_alg_sha512_224():
    assert get_hash_alg("main.py",
                        "sha512_224") == "9a5d64ed6443080a4e3a64ff60b8f014bba4d463276b0c10e69cbe77  main.py"


def test_get_hash_alg_whirlpool():
    assert get_hash_alg("main.py",
                        "whirlpool") == "95617de8b56c54c170df316cc95786674f34e6eef57e819079d882abf0421ce987dc19f66e03c6f3eab6b31f49af0b2a57b2567e054f41faea974769ef0bc252  main.py"


def test_get_hash_alg_ripemd160():
    assert get_hash_alg("main.py",
                        "ripemd160") == "d041802baf43e7454c90b85f4292bc06f008e3d6  main.py"


def test_get_hash_alg_sha512_256():
    assert get_hash_alg("main.py",
                        "sha512_256") == "9fe6cb9bf8d9d1abd375b7c167018cb327daf21aacc1427346f77c5dda0e91e3  main.py"


def test_get_hash_alg_md4():
    assert get_hash_alg("main.py",
                        "md4") == "814ce90b304991bd052fda59e0d74838  main.py"


def test_get_hash_alg_sm3():
    assert get_hash_alg("main.py",
                        "sm3") == "c537a0210f88ddd071a0f462bb5099688c393a7d05b8aab049929f9a00ded28e  main.py"


def test_get_hash_alg_md5_sha1():
    assert get_hash_alg("main.py",
                        "md5-sha1") == "a12382dd04e3c6576de6b9734abef21001300550040e197e2c936d41b56a4fd50fb0fdc3  main.py"
