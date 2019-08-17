import json
import pprint

if __name__ == '__main__':
    filename = 'data/active/aqrate'
    with open(filename,'r') as f:
        for line in f.readlines():
            data = json.loads(line)
            pprint.pprint(data)


# class FreqStack:
#
#     def __init__(self):
#         self.count = collections.defaultdict(int)
#         self.stack = []
#
#     def push(self, x: int) -> None:
#         self.stack.append(x)
#         self.count[x] += 1
#
#     def pop(self) -> int:
#         mf = float('-inf')
#         for _,v in self.count.items():
#             mf = max(mf, v)
#         cand = set([k for k,v in self.count.items() if v == mf])
#         for i in reversed(range(len(self.stack))):
#             if self.stack[i] in cand:
#                 self.count[self.stack[i]] -= 1
#                 return self.stack.pop(i)
#
#
# # Your FreqStack object will be instantiated and called as such:
# # obj = FreqStack()
# # obj.push(x)
# # param_2 = obj.pop()