def formula(val, num):
    l = len(val)
    print(l)
    if l == 2:
        if val == "11": return "1'b1"
        elif val == "01": return f"x[{num}]"
        elif val == "10": return f"~x[{num}]"
        else: return "1'b0"
    d0 = val[:int(l/2)]
    d1 = val[int(l/2):]
    if d0 == d1:
        return formula(d1, num + 1)
    return f"~x[{num}] & ({formula(d0, num + 1)}) | x[{num}] & ({formula(d1, num + 1)})"
    

val = input()

print(formula(val, 0))