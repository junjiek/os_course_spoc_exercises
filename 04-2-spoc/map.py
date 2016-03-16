PDE_BASE = 0xd80


def init_storage(filename):
    mem = []
    for line in open(filename):
        inputs = line.strip().split(':')[1].strip().split()
        for cont in inputs:
            mem.append(int(cont, 16))
    return mem


def get_mem(base, index, mem):
    return mem[base + index]


def handle_virtual(va):
    print 'Virtual Address 0x%x:' % va

    mem = init_storage('memory.in')
    disk = init_storage('disk.in')

    pde_index = (va & 0x7c00) >> 10
    pte_index = (va & 0x3e0) >> 5
    offset = va & 0x1f

    pde_content = get_mem(PDE_BASE, pde_index, mem)
    pde_valid = pde_content >> 7
    pte_base = pde_content - (pde_valid << 7)

    print '\t--> pde index: 0x%x pde contents: (valid 0x%x, pfn 0x%x)' \
          % (pde_index, pde_valid, pte_base)

    if not pde_valid:
        print '\t\t--> Fault (page directory entry not valid)'
        return

    pte_content = get_mem(pte_base << 5, pte_index, mem)
    pte_valid = pte_content >> 7
    phys_base = pte_content - (pte_valid << 7)

    print '\t\t--> pte index: 0x%x pte contents: (valid 0x%x, pfn 0x%x)' \
          % (pte_index, pte_valid, phys_base)

    if not pte_valid:
        if phys_base != 0x7f:
            disk_content = get_mem(phys_base << 5, offset, disk)
            print '\t\t\t--> To Disk Sector Address 0x%x --> Value 0x%x' \
                  % ((phys_base << 5) + offset, disk_content)
        else:
            print '\t\t\t -> Fault (page table entry not valid)'
        return

    phys_content = get_mem(phys_base << 5, offset, mem)
    print '\t\t\t--> To Physical Address 0x%x --> Value: 0x%x' \
          % ((phys_base << 5) + offset, phys_content)

if __name__ == '__main__':
    for line in open('virtual_addr.in'):
        handle_virtual(int(line.strip().split()[2], 16))
