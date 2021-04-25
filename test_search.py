from functools import lru_cache


def my_dist_cached(a, b):
    @lru_cache(maxsize=len(a) * len(b))
    def recursive(i, j):
        if i == 0 or j == 0:
            return max(i, j)
        elif a[i - 1] == b[j - 1]:
            return recursive(i - 1, j - 1)
        else:
            return 1 + min(
                recursive(i, j - 1),
                recursive(i - 1, j),
                recursive(i - 1, j - 1)
            )
    return recursive(len(a), len(b))


str1 = "Что такое словари"
str2 = "Словари в пайтон, как создать словарь?"
lev = my_dist_cached("hello world", "bye world!")
bigger = max([len(str1), len(str2)])
pct = ((bigger - lev) / bigger) * 100
print(pct)