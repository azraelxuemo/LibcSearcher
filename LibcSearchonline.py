#!/usr/bin/python3
import requests, re

API = "https://libc.nullbyte.cat/"


class LibcSearcher:
    def __init__(self, symbol_name: str = None, address: int = None):
        self.libc_list = []
        self.the_libc = None
        if (symbol_name is not None) and (address is not None):
            self.query_libc(symbol_name, address)
        self.show_libcs()

    def query_libc(self, symbol_name, address):
        result = requests.get(f"{API}?q={symbol_name}:{hex(address)}")
        match_libcs = re.findall(
            f'<a class="lib-item ">([\d\w\s\.-]*?)</a>',
            result.text,
        )
        if len(match_libcs):
            for lib in match_libcs:
                self.libc_list.append(lib.strip())

    def show_libcs(self):
        if self.libc_list == []:
            print("\x1b[1;31m" + "[+] No libc satisfies constraints." + "\x1b[0m")
            exit(0)

        elif len(self.libc_list) == 1:
            self.the_libc = self.libc_list[0]
        else:
            print(
                "\x1b[33m"
                + "[+] There are multiple libc that meet current constraints :"
                + "\x1b[0m"
            )
            self.select_libc()

    def select_libc(self, chosen_index: int = -1):
        if chosen_index == -1:
            for index, libc in enumerate(self.libc_list):
                print(str(index) + " - " + libc)
            chosen_index = input("\x1b[33m" + "[+] Choose one : " + "\x1b[0m")
        try:
            self.the_libc = self.libc_list[int(chosen_index)]
        except IndexError:
            print("\x1b[1;31m" + "[+] Index out of bound!" + "\x1b[0;m")
            self.select_libc()

    def dump(self, symbol_name: str) -> int:
        result = requests.get(f"{API}/d/{self.the_libc}.symbols")
        for name_addr in result.text.split("\n")[:-1]:
            name, addr = name_addr.split(" ")
            if name == symbol_name:
                return int(addr, 16)
