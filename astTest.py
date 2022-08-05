import astpretty
import ast
src = '''
def swap(a, b):
    boat = a
    a = b
    b = boat

arr = [10, 7, 3, 1, 6]
for i in range(len(arr) - 1):
    for j in range(len(arr) - i):
        if(arr[j] > arr[j + 1]):
            swap(arr[j], arr[j + 1])
'''
node = ast.parse(src, filename='<unknown>', mode="exec")
# astpretty.pprint(node)
print(ast.dump(node))
