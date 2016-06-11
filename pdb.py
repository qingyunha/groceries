# encoding=utf-8
import sys
import linecache

"""
Python的调试器pdb是通过sys.settrace注册trace函数完成的。

(https://docs.python.org/2/library/sys.html#sys.settrace)
Set the system’s trace function, which allows you to implement a Python source
code debugger in Python. The function is thread-specific; for a debugger to 
support multiple threads, it must be registered using settrace() for each 
thread being debugged.

Trace functions should have three arguments: frame, event, and arg. frame is
the current stack frame. event is a string: 'call', 'line', 'return', 
'exception', 'c_call', 'c_return', or 'c_exception'. arg depends on the event type.

The trace function is invoked (with event set to 'call') whenever a new local
scope is entered; it should return a reference to a local trace function to be
used that scope, or None if the scope shouldn’t be traced.

The local trace function should return a reference to itself (or to another 
function for further tracing in that scope), or None to turn off tracing 
in that scope.

我的理解：
这里提到两种trace函数，trace和local trace。trace在函数调用时被调用，或者说新的
frame创建时调用，即'call'事件，它应该返回local trace或者None。local_trace在函数内
或者说frame内调用，比如执行下一行代码的'line'事件。它应该返回local trace通常是
它本身或者None

另外frame对象中有一个属性f_trace记录着local trace
"""

def trace(frame, event, arg):
    if event == "line":
        fn = frame.f_code.co_filename
        line = linecache.getline(fn, frame.f_lineno)
        print line
        
        while True:
            try:
                exp = raw_input("(debug): ")
                if exp.startswith("next"):
                    return trace
                elif exp.startswith("print"):
                    _, exp = exp.split()
                    print eval(exp, frame.f_globals, frame.f_locals)
                else:
                    print "exec ", exp, "in ", frame.f_locals
                    exec exp in frame.f_globals, frame.f_locals
            except Exception as e:
                print "error: %s" % e
    return trace


def traceforissue5215(frame, event, arg):
    # http://bugs.python.org/issue5215#msg85105
    # 在一个trace函数中只保存对frame.f_locals的最后一次修改
    if event == "line":
        fn = frame.f_code.co_filename
        line = linecache.getline(fn, frame.f_lineno)
        print line
        
        cur_locals = frame.f_locals
        while True:
            try:
                exp = raw_input("(debug): ")
                if exp.startswith("next"):
                    return traceforissue5215
                elif exp.startswith("print"):
                    _, exp = exp.split()
                    print eval(exp, frame.f_globals, cur_locals)
                else:
                    exec exp in frame.f_globals, cur_locals
            except Exception as e:
                print "error: %s" % e
    return traceforissue5215

if __name__ == "__main__":

    def f():
        a = 1
        b = 1
        c = a + b
        print c
    # sys.settrace(trace)
    sys.settrace(traceforissue5215)

    f()
