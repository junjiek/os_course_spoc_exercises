// Implementation of malloc/free using first-fit
// 
// Created by: Junjie Ke 2012011335, Chenghui Zhao 2012011384

#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>

union header {
  struct {
    union header *ptr;
    unsigned int size;
  } s;
  long x;
};

typedef union header Header;

static Header base;
static Header *freep;

void myfree(void *ap) {
  Header *bp, *p;

  bp = (Header*)ap - 1;
  for (p = freep; !(bp > p && bp < p->s.ptr); p = p->s.ptr) {
    if (p >= p->s.ptr && (bp > p || bp < p->s.ptr)) {
      break;
    }
  }
  if (bp + bp->s.size == p->s.ptr) {
    bp->s.size += p->s.ptr->s.size;
    bp->s.ptr = p->s.ptr->s.ptr;
  } else
    bp->s.ptr = p->s.ptr;
  if (p + p->s.size == bp) {
    p->s.size += bp->s.size;
    p->s.ptr = bp->s.ptr;
  } else
    p->s.ptr = bp;
  freep = p;
}

static Header* morecore(unsigned int nu) {
  char *p;
  Header *hp;

  if(nu < 4096)
    nu = 4096;
  p = (char*) sbrk(nu * sizeof(Header));
  if(p == (char*) - 1)
    return 0;
  hp = (Header*)p;
  hp->s.size = nu;
  myfree((void*)(hp + 1));
  return freep;
}

void* mymalloc(unsigned int nbytes) {
  Header *p, *prevp;
  unsigned int nunits;

  nunits = (nbytes + sizeof(Header) - 1) / sizeof(Header) + 1;
  if ((prevp = freep) == 0){
    base.s.ptr = freep = prevp = &base;
    base.s.size = 0;
  }
  for (p = prevp->s.ptr; ; prevp = p, p = p->s.ptr){
    if (p->s.size >= nunits){
      if (p->s.size == nunits) {
        prevp->s.ptr = p->s.ptr;
      } else {
        p->s.size -= nunits;
        p += p->s.size;
        p->s.size = nunits;
      }
      freep = prevp;
      return (void*)(p + 1);
    }
    if (p == freep) {
      if ((p = morecore(nunits)) == 0) {
        return 0;
      }
    }
  }
}

void memtest(void) {
  void *m1, *m2;
  printf("mem test.\n");
  m1 = 0;
  while ((m2 = mymalloc(10001)) != 0){
    *(char**)m2 = m1;
    m1 = m2;
  }
  while (m1) {
    m2 = *(char**)m1;
    myfree(m1);
    m1 = m2;
  }
  m1 = mymalloc(1024*20);
  if (m1 == 0){
    printf("couldn't allocate mem?!!\n");
    return;
  }
  myfree(m1);
  printf("mem test passed.\n");
  return;
}

int main(int argc, char *argv[]) {
  memtest();
  return 0;
}