# LibcSearcher
a more powerfull online LibcSearch

How to use

from LibcSearcheronline import LibcSearcher

write_addr=0

libc=LibcSearcher("write",write_addr)

libc.dump("read")

libc.dump("str_bin_sh")
