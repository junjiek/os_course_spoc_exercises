##（spoc)了解race condition. 进入[race-condition代码目录](https://github.com/chyyuu/ucore_lab/tree/master/related_info/lab7/race-condition)。

 - 执行 `./x86.py -p loop.s -t 1 -i 100 -R dx`， 请问`dx`的值是什么？
 
        dx初始为0，循环1次之后`dx = -1 < 0`
        
 - 执行 `./x86.py -p loop.s -t 2 -i 100 -a dx=3,dx=3 -R dx` ， 请问`dx`的值是什么？
        
        dx初始为3，然后开始循环直到`dx < 0`，然后跳到第二个线程开始执行，因此最后dx = -1
        
 - 执行 `./x86.py -p loop.s -t 2 -i 3 -r -a dx=3,dx=3 -R dx`， 请问`dx`的值是什么？
        
        -r参数导致中断是随机的，每次都不相同，产生了race-condition。最终`dx = -1`。其中一次输出结果为：
```
   dx          Thread 0                Thread 1         
    3   
    2   1000 sub  $1,%dx
    3   ------ Interrupt ------  ------ Interrupt ------  
    2                            1000 sub  $1,%dx
    2   ------ Interrupt ------  ------ Interrupt ------  
    2   1001 test $0,%dx
    2   ------ Interrupt ------  ------ Interrupt ------  
    2                            1001 test $0,%dx
    2   ------ Interrupt ------  ------ Interrupt ------  
    2   1002 jgte .top
    2   ------ Interrupt ------  ------ Interrupt ------  
    2                            1002 jgte .top
    2   ------ Interrupt ------  ------ Interrupt ------  
    1   1000 sub  $1,%dx
    2   ------ Interrupt ------  ------ Interrupt ------  
    1                            1000 sub  $1,%dx
    1   ------ Interrupt ------  ------ Interrupt ------  
    1   1001 test $0,%dx
    1   1002 jgte .top
    0   1000 sub  $1,%dx
    1   ------ Interrupt ------  ------ Interrupt ------  
    1                            1001 test $0,%dx
    0   ------ Interrupt ------  ------ Interrupt ------  
    0   1001 test $0,%dx
    1   ------ Interrupt ------  ------ Interrupt ------  
    1                            1002 jgte .top
    0                            1000 sub  $1,%dx
    0                            1001 test $0,%dx
    0   ------ Interrupt ------  ------ Interrupt ------  
    0   1002 jgte .top
    0   ------ Interrupt ------  ------ Interrupt ------  
    0                            1002 jgte .top
   -1                            1000 sub  $1,%dx
   -1                            1001 test $0,%dx
    0   ------ Interrupt ------  ------ Interrupt ------  
   -1   1000 sub  $1,%dx
   -1   1001 test $0,%dx
   -1   1002 jgte .top
   -1   ------ Interrupt ------  ------ Interrupt ------  
   -1                            1002 jgte .top
   -1                            1003 halt
   -1   ----- Halt;Switch -----  ----- Halt;Switch -----  
   -1   ------ Interrupt ------  ------ Interrupt ------  
   -1   1003 halt
```
    
 - 变量x的内存地址为2000, `./x86.py -p looping-race-nolock.s -t 1 -M 2000`, 请问变量x的值是什么？
        
        由输出知变量x最后为1
```
        2000          Thread 0         
        0   
        0   1000 mov 2000, %ax
        0   1001 add $1, %ax
        1   1002 mov %ax, 2000
        1   1003 sub  $1, %bx
        1   1004 test $0, %bx
        1   1005 jgt .top
        1   1006 halt
```
        
        
 - 变量x的内存地址为2000, `./x86.py -p looping-race-nolock.s -t 2 -a bx=3 -M 2000`, 请问变量x的值是什么？为何每个线程要循环3次？
    
        x = 6。因为初始时bx为3，而线程每循环一次就将bx减1并与0比较。
        输出结果如下：

```
2000          Thread 0                Thread 1         
    0   
    0   1000 mov 2000, %ax
    0   1001 add $1, %ax
    1   1002 mov %ax, 2000
    1   1003 sub  $1, %bx
    1   1004 test $0, %bx
    1   1005 jgt .top
    1   1000 mov 2000, %ax
    1   1001 add $1, %ax
    2   1002 mov %ax, 2000
    2   1003 sub  $1, %bx
    2   1004 test $0, %bx
    2   1005 jgt .top
    2   1000 mov 2000, %ax
    2   1001 add $1, %ax
    3   1002 mov %ax, 2000
    3   1003 sub  $1, %bx
    3   1004 test $0, %bx
    3   1005 jgt .top
    3   1006 halt
    3   ----- Halt;Switch -----  ----- Halt;Switch -----  
    3                            1000 mov 2000, %ax
    3                            1001 add $1, %ax
    4                            1002 mov %ax, 2000
    4                            1003 sub  $1, %bx
    4                            1004 test $0, %bx
    4                            1005 jgt .top
    4                            1000 mov 2000, %ax
    4                            1001 add $1, %ax
    5                            1002 mov %ax, 2000
    5                            1003 sub  $1, %bx
    5                            1004 test $0, %bx
    5                            1005 jgt .top
    5                            1000 mov 2000, %ax
    5                            1001 add $1, %ax
    6                            1002 mov %ax, 2000
    6                            1003 sub  $1, %bx
    6                            1004 test $0, %bx
    6                            1005 jgt .top
    6                            1006 halt

```
        
        
 - 变量x的内存地址为2000, `./x86.py -p looping-race-nolock.s -t 2 -M 2000 -i 4 -r -s 0`， 请问变量x的值是什么？
    
        x = 1或2
 
 - 变量x的内存地址为2000, `./x86.py -p looping-race-nolock.s -t 2 -M 2000 -i 4 -r -s 1`， 请问变量x的值是什么？
 
        x = 1或2
        
 - 变量x的内存地址为2000, `./x86.py -p looping-race-nolock.s -t 2 -M 2000 -i 4 -r -s 2`， 请问变量x的值是什么？ 
    
        x = 1或2
 
 - 变量x的内存地址为2000, `./x86.py -p looping-race-nolock.s -a bx=1 -t 2 -M 2000 -i 1`， 请问变量x的值是什么？ 
 
        x = 1