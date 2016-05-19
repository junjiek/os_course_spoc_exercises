
1）小组思考题(1-键盘输入)：描述ucore操作系统中“键盘输入”从请求到完成的整个执行过程，并分析I/O过程的时间开销。

用户在键盘进行输入，触发KBD中断，在trap.c的trap_dispatch()进行处理，其中断号为IRQ_KBD。

```
    case IRQ_OFFSET + IRQ_KBD:
        c = cons_getc();
        {
          extern void dev_stdin_write(char c);
          dev_stdin_write(c);
        }
        break;
```

调用con_getc()获取字符c，然后调用dev_stdin_write将字符c写入stdin缓冲区。 这时候如果有进程在等待键盘输入，就唤醒这个进程。

时间开销主要花费在进程的切换和检查等待队列上。