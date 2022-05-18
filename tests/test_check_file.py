from sha import HashFiles


class Test:
    def test_save_file(self):
        check = "hashes"
        check_file = HashFiles("", check, algorithm="sha256", processes=1)
        result = check_file.check_file(file=check)
        assert isinstance(result, list)
