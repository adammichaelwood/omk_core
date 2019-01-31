from utils.method_dispatch import methoddispatch

class TestClass():

    def __init__(self, arg):
        self.i = arg

    @methoddispatch
    def print_i(self):
        print(self.i)
    
    @print_i.register(int)
    def _(self, i):
        print(self.i*i)

    @print_i.register(str)
    def _(self, s):
        print(s)

if __name__ == "__main__":

    q = TestClass("og")

    print("Should be 'og':")
    q.print_i(1)

    print("Should be 'ogog'")
    q.print_i(2)

    print("Should be 'diff'")
    q.print_i('diff')