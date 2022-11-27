class Node:

    def __init__(self, data):
        self.data = data
        self.next = None


class Stack:  # Stack class using Linked List
    def __init__(self):
        self.head = None
        self.count = 0

    def __len__(self):
        return self.count

    def is_empty(self):
        return self.count == 0

    def push(self, data: object):
        newNode = Node(data)
        if self.head is None:
            self.head = newNode
        else:
            newNode.next = self.head
            self.head = newNode
        self.count = self.count + 1

    def pop(self):
        if self.head is None:
            return -1
        data = self.head.data
        self.head = self.head.next
        self.count = self.count - 1
        return data

    def top(self):
        if self.head is None:
            return -1
        data = self.head.data
        return data


class Vector:
    def __init__(self, x, y, z, d):
        self.x = x
        self.y = y
        self.z = z
        self.d = d

    def add(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z, self.d + other.d)

    def mul(self, other):
        return Vector(other * self.x, other * self.y, other * self.z, other * self.d)

    def printVector(self):
        return [self.x, self.y, self.z, self.d]


def reader(s):  # O(n)
    i = 0
    origin = Vector(0, 0, 0, 0)
    while i < len(s):  # O(n)
        j = i + 1
        if s[i] == '+':
            if s[j] == 'X':
                origin = origin.add(Vector(1, 0, 0, 1))
            if s[j] == 'Y':
                origin = origin.add(Vector(0, 1, 0, 1))
            if s[j] == 'Z':
                origin = origin.add(Vector(0, 0, 1, 1))

        if s[i] == '-':
            if s[j] == 'X':
                origin = origin.add(Vector(-1, 0, 0, 1))
            if s[j] == 'Y':
                origin = origin.add(Vector(0, -1, 0, 1))
            if s[j] == 'Z':
                origin = origin.add(Vector(0, 0, -1, 1))
        i += 2
    return origin


def isAlphabet(s):
    if s in 'XYZ':
        return True
    return False


def isOperator(s):
    if s in '+-':
        return True
    return False


def isNumeric(s):
    if s in '1234567890':
        return True
    return False


def isOpenBracket(s):
    if s == '(':
        return True
    return False


def isCloseBracket(s):
    if s == ')':
        return True
    return False


def number(s):
    # a=''
    # for elt in s:
    #     a+=elt
    # return (s)
    stack = Stack()
    for elt in s:
        # if isNumeric:
        '''no need for the above conditional as it will always be isNumeric'''
        stack.push(elt)
        '''eg- if we encounter 2351 in input then we first push 2 then 3 then 5 and then 1 into stack'''
    i = 0
    ans = 0
    while stack.__len__() != 0:  # until stack isn't empty
        ans += int(stack.pop()) * (10 ** i)
        '''in the above eg the stack will look like -> [2,3,5,1]
        now we pop 1 and since i is initialised to 0, 10**0==1 and hence 1*1=1
        then pop 5 and as i==1, 5*10**1=50
        so on we keep adding the place values to get the final no.
        2000+300+50+1==2351'''
        i += 1

    return ans


def findPositionandDistance(P):
    stack = Stack()
    stack.push(1)  # so that if no nested brackets exist, reader(P[i:i+2]) * stack.top() doesnt raise Error
    origin = Vector(0, 0, 0, 0)
    i = 0
    P = '(' + P + ')'  # to maintain edge cases
    while i < len(P):  # O(n)

        if isOperator(P[i]):  # O(1)
            '''if first elt is + or - & the second is X, Y or Z then it corresponds to a unit vector in respective axes,
             so we make a base case vector i.e. origin that takes on all these unit vectors and sums them '''
            origin = origin.add(reader(P[i:i + 2]).mul(int(stack.top())))  # O(1)
            '''reader(P[i:i + 2])) then gets multiplied with the top of the stack i.e. the no. preceding the
            string and finally gets stored as the final evaluated origin. eg- in 2(+X), +X is (1,0,0) which when 
            multiplied with 2 (which is the top of the stack as only numerics are getting pushed), returns (2,0,0)'''
            i += 1

        if isAlphabet(P[i]):  # O(1)
            '''if we encounter a naked X, Y or Z without its sign then its of no use and we skip to the next element'''
            i += 1

        if isNumeric(P[i]):  # O(1) the principle index i will get replaced by j and will continue until i takes over
            j = 0
            '''if we encounter a numeric value, we run a lookahead variable j in a loop that goes forward until we
            encounter something that ISN'T a number.'''
            while isNumeric(P[i + j]):  # O(1) as i will freeze here and will get instantly updated later by i + j
                j += 1
                ''' This variable j will act as a counter and will give the length of the numeric before a '(' '''
            stack.push(number(P[i:i + j]) * int(stack.top()))
            '''now we multiply the evaluated no. with the previous top and push it in stack. eg- 2(3(+X))==6(+X)'''
            i = i + j  # O(1) as i isn't incrementing in indexes already indexed by lookahead variable j
            '''i is updated to the position its lookahead variable i+j reached so as to not repeat the iteration'''
            i += 1

        if isOpenBracket(P[i]):  # O(1)
            '''no need to do anything with the open bracket'''
            i += 1

        if isCloseBracket(P[i]):  # O(1)
            '''the detection of a '(' signifies the end of a paranthesis, i.e. the vector and the numeric multiplied 
            with it have been processed and have been added to the final origin. Hence the top of stack now is of no use
            and must be popped'''
            stack.pop()  # O(1)
            i += 1

    return origin.printVector()  # O(n) is the time complexity