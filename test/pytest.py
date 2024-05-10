from ..testcases.dummy import Counter


def test_1():
    x = Counter(10)
    assert x.report() == 10
    assert x.report() == 10

print("hello")

x = Counter(10)
print(x.report())