#!/usr/bin/env python3

class Packet:
    def __init__(self, hex_code):   
        print('-----')     
        self.hex_code = hex_code
        print(self.hex_code)

        self.length = 0
        self.value = None
        self.packets = []

        self.parser = {
            0: self.parse_operator,
            1: self.parse_operator,
            2: self.parse_operator,
            3: self.parse_operator,
            4: self.parse_literal,
            5: self.parse_operator,
            6: self.parse_operator,
            7: self.parse_operator,
        }
        self.parse()

    def unbin(self, start, end):
        return int(''.join(self.bits[start:end]), 2)

    def hexify(self, start, end):
        if -1 == end:
            end = len(self.bits)+1
        bits = self.bits[start:end]
        for i in range(len(bits)%4):
            bits += '0'
        output = ''
        for index in range(0, end-start, 4):
            nibble = ''.join(bits[index:index+4])
            if nibble:
                output += hex(int(nibble,2))[-1]
        while (end-start)/4 > len(output):
            output += '0'
        return output

    def parse(self):
        self.bits = list(bin(int(self.hex_code, 16))[2:])
        pad_length = 4*len(self.hex_code) - len(self.bits)
        for i in range(pad_length):
            self.bits.insert(0, '0')
        print(''.join(self.bits))

        self.version = self.unbin(0,3)
        print(f'version: {self.version}')
        self.type = self.unbin(3,6)
        print(f'type: {self.type}')
        self.parser[self.type]()

    def parse_literal(self):
        done = False
        index = 6
        value_bits = []
        self.length = index
        while not done:
            bits = self.bits[index:index+5]
            index += 5
            value_bits += bits[1:]
            done = (bits[0] == '0')
            self.length += 5
        self.value = int(''.join(value_bits), 2)
        print(f'value: {self.value}')
        
    def parse_operator(self):
        index = 6
        self.type_id = self.unbin(index,index+1)
        index += 1
        print(f'type_id: {self.type_id}')
        
        if 0 == self.type_id:
            subpacket_length = self.unbin(index,index+15)
            print(f'subpacket_length: {subpacket_length}')
            index += 15
            self.length = index + subpacket_length
            while index < self.length:
                next_hex = self.hexify(index,-1)
                next_packet = Packet(next_hex)
                self.packets.append(next_packet)
                index += next_packet.length
        else:
            num_subpackets = self.unbin(index,index+11)
            print(f'num_subpackets {num_subpackets}')
            index += 11
            subpacket_length = 0
            self.length = index
            while num_subpackets > 0:
                num_subpackets -= 1
                next_hex = self.hexify(index,-1)
                next_packet = Packet(next_hex)
                self.packets.append(next_packet)
                index += next_packet.length
                self.length += next_packet.length

        self.do_operation()

    def do_operation(self):
        values = [packet.value for packet in self.packets]
        if self.type == 0:
            self.value = sum(values)
        elif self.type == 1:
            self.value = 1
            for value in values:
                self.value *= value
        elif self.type == 2:
            self.value = min(values)
        elif self.type == 3:
            self.value = max(values)
        elif self.type == 5:
            self.value = 1 if values[0] > values[1] else 0
        elif self.type == 6:
            self.value = 1 if values[0] < values[1] else 0
        elif self.type == 7:
            self.value = 1 if values[0] == values[1] else 0
        print(f'value: {self.value}')

    def version_sum(self):
        total = self.version
        for packet in self.packets:
            total += packet.version_sum()
        return total

    def __str__(self):
        return str((self.version, self.type, self.length, self.value, self.packets, self.version_sum()))
    
    def __repr__(self):
        return str(self)

if '__main__' == __name__:
    lines = [
        'D2FE28',
        '38006F45291200',
        'EE00D40C823060',
        '8A004A801A8002F478',
        '620080001611562C8802118E34',
        'C0015000016115A2E0802F182340',
        'A0016C880162017C3686B18A3D4780',
        'C200B40A82',
        '04005AC33890',
        '880086C3E88112',
        'CE00C43D881120',
        'D8005AC2A8F0',
        'F600BC2D8F',
        '9C005AC2F8F0',
        '9C0141080250320F1802104A08',
    ]
    for line in lines:
        print('-'*80)
        packet = Packet(line)
        print(packet)
