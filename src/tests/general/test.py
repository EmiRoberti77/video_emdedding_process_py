range_vals = range(2, 5)
print(range_vals)
[print(v) for v in range_vals]
squares = [x * x for x in range_vals]
print(squares)
unique_lengths = {len(word) for word in ["ciao Emi, come stai?"]}
print(unique_lengths)

