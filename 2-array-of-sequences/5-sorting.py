fruits = ['apple', 'banana', 'cherry']
sorted_fruits = sorted(fruits) # created a new list
sorted_fruits_in_place = fruits.sort() # sorted the original list in place

print(sorted(fruits, key=len)) # sorts by length of the fruit names