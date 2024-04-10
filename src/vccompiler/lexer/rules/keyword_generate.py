keywords = ('boolean', 'break', 'continue', 'else', 'for', 'float', 'if', 'int', 'return', 'void', 'while')
max_keyword_length = max(len(keyword) for keyword in keywords)
map_state = [""]
other_state = [""]

for i in range(0, max_keyword_length):
    keydivide = [keyword[:i+1] if i < len(keyword) else "" for keyword in keywords]
    keyset = set(keydivide)
    keyset.discard("")
    print("#", keyset)

    for char in keyset:
        pre_state = 0 if len(map_state) == 1 else map_state.index(char[:-1])
        print("#index", char[:-1])
        print(f"state{len(map_state)} = State({len(map_state)})")
        print(f"state{pre_state}.add('{char[-1]}', state{len(map_state)})")
        map_state.append(char)
        if pre_state != 0:
            print(f"state{pre_state}.add(alias[\"letter\"] + alias[\"digit\"],state{99})")

    print()

