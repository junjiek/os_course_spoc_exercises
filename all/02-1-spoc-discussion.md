#lec 3 SPOC Discussion

##**提前准备**
（请在周一上课前完成）

 - 完成lec3的视频学习和提交对应的在线练习
 - git pull ucore_os_lab, v9_cpu, os_course_spoc_exercises  　in github repos。这样可以在本机上完成课堂练习。
 - 仔细观察自己使用的计算机的启动过程和linux/ucore操作系统运行后的情况。搜索“80386　开机　启动”
 - 了解控制流，异常控制流，函数调用,中断，异常(故障)，系统调用（陷阱）,切换，用户态（用户模式），内核态（内核模式）等基本概念。思考一下这些基本概念在linux, ucore, v9-cpu中的os*.c中是如何具体体现的。
 - 思考为什么操作系统需要处理中断，异常，系统调用。这些是必须要有的吗？有哪些好处？有哪些不好的地方？
 - 了解在PC机上有啥中断和异常。搜索“80386　中断　异常”
 - 安装好ucore实验环境，能够编译运行lab8的answer
 - 了解Linux和ucore有哪些系统调用。搜索“linux 系统调用", 搜索lab8中的syscall关键字相关内容。在linux下执行命令: ```man syscalls```
 - 会使用linux中的命令:objdump，nm，file, strace，man, 了解这些命令的用途。
 - 了解如何OS是如何实现中断，异常，或系统调用的。会使用v9-cpu的dis,xc, xem命令（包括启动参数），分析v9-cpu中的os0.c, os2.c，了解与异常，中断，系统调用相关的os设计实现。阅读v9-cpu中的cpu.md文档，了解汇编指令的类型和含义等，了解v9-cpu的细节。
 - 在piazza上就lec3学习中不理解问题进行提问。

## 第三讲 启动、中断、异常和系统调用-思考题

## 3.1 BIOS
 1. 比较UEFI和BIOS的区别。

UEFI是“统一的可扩展固件接口”，是一种详细描述全新类型接口的标准，是适用于电脑的标准固件接口，是BIOS的一种升级替代方案。UEFI启动对比BIOS启动的优势有三点：安全性更强、启动配置更灵活、支持容量更大。

 1. 描述PXE的大致启动流程。

PXE加电之后进行自检，然后通过网络协议向服务器请求加载开机映像文件，从而启动机器。

## 3.2 系统启动流程
 1. 了解NTLDR的启动流程。

NTLDR是windows NT等操作系统的加载程序。
启动流程为：装入NTLDR，把计算机的微处理器从实模式转变为32位平面内存模式，开始执行适当的小型文件系统驱动程序，读取装载的配置文件，硬件检测，然后装入windows操作系统。

 1. 了解GRUB的启动流程。

GRUB装入之后，读取装载的配置文件menu.lst，建立要载入的菜单列表，显示引导菜单，装入操作系统程序。

 1. 比较NTLDR和GRUB的功能有差异。

NTLDR只能安装在硬盘中，只能引导windows系统。而GRUB可以安装在U盘，硬盘，光盘等，可用于引导多种系统。

 1. 了解u-boot的功能。

u-boot是通用的计算机引导程序，可以适用于于不同的计算机架构，比如X86, MIPS, ARM等。

## 3.3 中断、异常和系统调用比较
<<<<<<< HEAD
 1. 举例说明Linux中有哪些中断，哪些异常？

Linux中断有时钟中断、串口中断等；异常包括除零错、非法访问地址等。

 1. Linux的系统调用有哪些？大致的功能分类有哪些？  (w2l1)
=======
 1. 什么是中断、异常和系统调用？
 2. 中断、异常和系统调用的处理流程有什么异同？
 2. 举例说明Linux中有哪些中断，哪些异常？
 3. 以ucore lab8的answer为例，uCore的时钟中断处理流程。
 1. Linux的系统调用有哪些？大致的功能分类有哪些？  (w2l1)

 ```
  + 采分点：说明了Linux的大致数量（上百个），说明了Linux系统调用的主要分类（文件操作，进程管理，内存管理等）
  - 答案没有涉及上述两个要点；（0分）
  - 答案对上述两个要点中的某一个要点进行了正确阐述（1分）
  - 答案对上述两个要点进行了正确阐述（2分）
  - 答案除了对上述两个要点都进行了正确阐述外，还进行了扩展和更丰富的说明（3分）
 ```
>>>>>>> c0d9f5dc04f7811a6d7641dd0a6c7e1f9461cdf3
 
Linux包含了200多个系统调用。主要分类包括文件操作、进程管理、内存管理等。文件操作的系统调用主要为对硬件文件和标准输出的管理，包括读操作、写操作等；进程管理的系统调用主要用来保证操作系统能够在多进程环境下正常运作，常用的系统调用功能包括fork clone exit等等，用户在编写多进程程序的时候会经常使用到；内存管理的系统调用主要包括在堆栈分配内存、回收内存、读写内存等操作。

 1. 以ucore lab8的answer为例，uCore的系统调用有哪些？大致的功能分类有哪些？(w2l1)
 
ucore包含20多个系统调用，定义在kern/syscall/syscall.c。根据功能可以分为文件操作（write read seek fstats等）、进程管理（exit fork wait exec等）和内存管理（pagedir等）。
 
## 3.4 linux系统调用分析
 1. 通过分析[lab1_ex0](https://github.com/chyyuu/ucore_lab/blob/master/related_info/lab1/lab1-ex0.md)了解Linux应用的系统调用编写和含义。(w2l1)

系统调用是操作系统提供给应用程序的服务接口。应用程序在使用系统调用的时候，程序转入内核态执行，操作系统在系统调用表中根据系统调用编号查询需要执行的系统调用，并执行相应的代码。

 ```
  - objdump可以将二进制文件反汇编为汇编代码，可以方便对目标文件进行汇编代码分析。
  - nm主要可以对目标文件中的符号进行可视化
  - file用于检测文件类型
  - strace追踪系统调用的情况，可以看到所有被调用的系统调用
 ```

2. 通过调试[lab1_ex1](https://github.com/chyyuu/ucore_lab/blob/master/related_info/lab1/lab1-ex1.md)了解Linux应用的系统调用执行过程。(w2l1)

strace用于观察程序执行过程中使用系统调用的情况，包括各种系统调用所占用的时间以及相应比例、调用的次数以及出现错误的次数等。使用strace命令看到，为了实现简单的hello world调用了很多系统调用进行初始化。首先进行进程初始化，然后进行文件的检查初始化，并设置需要使用的内存，然后才能输出hello world。

具体包括以下几个函数：

 ```
  - execve运行一个文件，在父进程中fork一个子进程，在子进程中调用exec函数启动新的程序。
  - access会检查是否可以读/写某一已存在的文件
  - open打开一个文件
  - fstat64获取文件状态
  - mmap2可以将某文件映射至内存(进程空间)，如此可以把对文件的操作转为对内存的操作。
  - set_thread_area在线程局部存储区域Thread Local Storage中设置了一个entry项
  - mprotect设置内存访问权限，可以用来修改一段指定内存区域的保护属性
  - munmap取消文件或者设备在内存中的映射
  - write输出字符串
  - exit_group退出进程中所有的线程
 ```

## 3.5 ucore系统调用分析
 1. ucore的系统调用中参数传递代码分析。
<<<<<<< HEAD

使用kern/trap/trap.h中定义的trapframe结构来传递参数。在trapframe中有pushregs结构的寄存器组tf_regs，pushregs的reg_eax传递系统调用号，reg_ebx，reg_ecx，reg_edi，reg_esi传递系统调用参数。

进行系统调用的函数定义在kern/trap/trap.c中。trap(trapframe)函数调用trap_dispatch(trapframe)，在trap_dispatch()中检查中断类型trapframe tf->trapno，如果是系统调用T_SYSCALL，则调用syscall()。

 1. ucore的系统调用中返回结果的传递代码分析。

/kern/trap/trapentry.S中的代码对系统调用返回进行处理，__trapret恢复存储在trapframe中的原有的CPU状态（包括恢复寄存器、清除trap number和error code），并调用iret从中断返回

=======
 1. 以getpid为例，分析ucore的系统调用中返回结果的传递代码。
>>>>>>> c0d9f5dc04f7811a6d7641dd0a6c7e1f9461cdf3
 1. 以ucore lab8的answer为例，分析ucore 应用的系统调用编写和含义。

用户在user/libs/syscall.c中对系统调用进行编写（如sys_exit、sys_fork等），统一调用syscall()函数。syscall()通过压栈，和定义在kern/syscall/syscall.c内联函数调用传入参数。

 1. 以ucore lab8的answer为例，尝试修改并运行ucore OS kernel代码，使其具有类似Linux应用工具`strace`的功能，即能够显示出应用程序发出的系统调用，从而可以分析ucore应用的系统调用执行过程。
 
## 3.6 请分析函数调用和系统调用的区别
 1. 请从代码编写和执行过程来说明。
   1. 说明`int`、`iret`、`call`和`ret`的指令准确功能
<<<<<<< HEAD

`int`是应用程序进行系统调用，执行过程是保存程序现场，切换特权级，切换堆栈，进入内核态，执行系统调用代码。

`iret`是从系统调用返回应用程序，执行过程是切换特权级，切换堆栈，进入用户态，恢复程序现场，并将返回结果压入堆栈。

`call`的功能是应用程序内部进行函数调用，执行过程是保存当前过程的现场，跳转至函数其实位置。

`ret`的功能是从子程序返回调用程序，执行过程是回复调用程序的现场，将函数返回结果压入堆栈，跳转回调用程序之前的地址。
=======
 

## v9-cpu相关题目
---

### 提前准备
```
cd YOUR v9-cpu DIR
git pull 
cd YOUR os_course_spoc_exercise DIR
git pull 
```

### v9-cpu系统调用实现
  1. v9-cpu中os4.c的系统调用中参数传递代码分析。
  1. v9-cpu中os4.c的系统调用中返回结果的传递代码分析。
  1. 理解v9-cpu中os4.c的系统调用编写和含义。

>>>>>>> c0d9f5dc04f7811a6d7641dd0a6c7e1f9461cdf3
