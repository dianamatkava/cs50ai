

if __name__ == "__main__":
    import runner




from time import perf_counter as pc

t1 = pc()
l = [i for i in range(1000000)]
print("list comp", pc() - t1)


t1 = pc()
l = []
for i in range(1000000):
    l.append(i)


print("list", pc() - t1)


t1 = pc()
l = {i: i for i in range(1000000)}
print("dict com", pc() - t1)


