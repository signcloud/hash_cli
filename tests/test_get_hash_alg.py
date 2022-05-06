from hash import get_hash_alg


def test_get_hash_alg_md5():
    assert (
        get_hash_alg("test_file", "md5")
        == "d41d8cd98f00b204e9800998ecf8427e  test_file"
    )


def test_get_hash_alg_sha512():
    assert (
        get_hash_alg("test_file", "sha512")
        == "cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e  test_file"
    )


def test_get_hash_alg_sha384():
    assert (
        get_hash_alg("test_file", "sha384")
        == "38b060a751ac96384cd9327eb1b1e36a21fdb71114be07434c0cc7bf63f6e1da274edebfe76f65fbd51ad2f14898b95b  test_file"
    )


def test_get_hash_alg():
    assert (
        get_hash_alg("test_file", "sha256")
        == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  test_file"
    )


def test_get_hash_alg_blake2s():
    assert (
        get_hash_alg("test_file", "blake2s")
        == "69217a3079908094e11121d042354a7c1f55b6482ca1a51e1b250dfd1ed0eef9  test_file"
    )


def test_get_hash_alg_sha3_512():
    assert (
        get_hash_alg("test_file", "sha3_512")
        == "a69f73cca23a9ac5c8b567dc185a756e97c982164fe25859e0d1dcc1475c80a615b2123af1f5f94c11e3e9402c3ac558f500199d95b6d3e301758586281dcd26  test_file"
    )


def test_get_hash_alg_sha3_384():
    assert (
        get_hash_alg("test_file", "sha3_384")
        == "0c63a75b845e4f7d01107d852e4c2485c51a50aaaa94fc61995e71bbee983a2ac3713831264adb47fb6bd1e058d5f004  test_file"
    )


def test_get_hash_alg_shake_256():
    assert (
        get_hash_alg("test_file", "shake_256")
        == "46b9dd2b0ba88d13233b3feb743eeb243fcd52ea62b81b82b50c27646ed5762fd75dc4ddd8c0f200cb05019d67b592f6fc821c49479ab48640292eacb3b7c4be141e96616fb13957692cc7edd0b45ae3dc07223c8e92937bef84bc0eab862853349ec75546f58fb7c2775c38462c5010d846c185c15111e595522a6bcd16cf86f3d122109e3b1fdd943b6aec468a2d621a7c06c6a957c62b54dafc3be87567d677231395f6147293b68ceab7a9e0c58d864e8efde4e1b9a46cbe854713672f5caaae314ed9083dab4b099f8e300f01b8650f1f4b1d8fcf3f3cb53fb8e9eb2ea203bdc970f50ae55428a91f7f53ac266b28419c3778a15fd248d339ede785fb  test_file"
    )


def test_get_hash_alg_sha224():
    assert (
        get_hash_alg("test_file", "sha224")
        == "d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f  test_file"
    )


def test_get_hash_alg_shake_128():
    assert (
        get_hash_alg("test_file", "shake_128")
        == "7f9c2ba4e88f827d616045507605853ed73b8093f6efbc88eb1a6eacfa66ef263cb1eea988004b93103cfb0aeefd2a686e01fa4a58e8a3639ca8a1e3f9ae57e235b8cc873c23dc62b8d260169afa2f75ab916a58d974918835d25e6a435085b2badfd6dfaac359a5efbb7bcc4b59d538df9a04302e10c8bc1cbf1a0b3a5120ea17cda7cfad765f5623474d368ccca8af0007cd9f5e4c849f167a580b14aabdefaee7eef47cb0fca9767be1fda69419dfb927e9df07348b196691abaeb580b32def58538b8d23f87732ea63b02b4fa0f4873360e2841928cd60dd4cee8cc0d4c922a96188d032675c8ac850933c7aff1533b94c834adbb69c6115bad4692d86  test_file"
    )


def test_get_hash_alg_sha3_224():
    assert (
        get_hash_alg("test_file", "sha3_224")
        == "6b4e03423667dbb73b6e15454f0eb1abd4597f9a1b078e3f5b5a6bc7  test_file"
    )


def test_get_hash_alg_sha1():
    assert (
        get_hash_alg("test_file", "sha1")
        == "da39a3ee5e6b4b0d3255bfef95601890afd80709  test_file"
    )


def test_get_hash_alg_blake2b():
    assert (
        get_hash_alg("test_file", "blake2b")
        == "786a02f742015903c6c6fd852552d272912f4740e15847618a86e217f71f5419d25e1031afee585313896444934eb04b903a685b1448b755d56f701afe9be2ce  test_file"
    )


def test_get_hash_alg_sha3_256():
    assert (
        get_hash_alg("test_file", "sha3_256")
        == "a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a  test_file"
    )


def test_get_hash_alg_sha512_224():
    assert (
        get_hash_alg("test_file", "sha512_224")
        == "6ed0dd02806fa89e25de060c19d3ac86cabb87d6a0ddd05c333b84f4  test_file"
    )


def test_get_hash_alg_whirlpool():
    assert (
        get_hash_alg("test_file", "whirlpool")
        == "19fa61d75522a4669b44e39c1d2e1726c530232130d407f89afee0964997f7a73e83be698b288febcf88e3e03c4f0757ea8964e59b63d93708b138cc42a66eb3  test_file"
    )


def test_get_hash_alg_ripemd160():
    assert (
        get_hash_alg("test_file", "ripemd160")
        == "9c1185a5c5e9fc54612808977ee8f548b2258d31  test_file"
    )


def test_get_hash_alg_sha512_256():
    assert (
        get_hash_alg("test_file", "sha512_256")
        == "c672b8d1ef56ed28ab87c3622c5114069bdd3ad7b8f9737498d0c01ecef0967a  test_file"
    )


def test_get_hash_alg_md4():
    assert (
        get_hash_alg("test_file", "md4")
        == "31d6cfe0d16ae931b73c59d7e0c089c0  test_file"
    )


def test_get_hash_alg_sm3():
    assert (
        get_hash_alg("test_file", "sm3")
        == "1ab21d8355cfa17f8e61194831e81a8f22bec8c728fefb747ed035eb5082aa2b  test_file"
    )


def test_get_hash_alg_md5_sha1():
    assert (
        get_hash_alg("test_file", "md5-sha1")
        == "d41d8cd98f00b204e9800998ecf8427eda39a3ee5e6b4b0d3255bfef95601890afd80709  test_file"
    )
