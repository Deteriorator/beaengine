#!/usr/bin/python
# -*- coding: utf-8 -*-
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#   
# @author : beaengine@gmail.com

from headers.BeaEnginePython import *
from nose.tools import *
import struct
import yaml

class TestSuite:

    def test_SimpleInstructions(self):
        stream = open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'opcode1byte.yml')), "r")
        instructions = yaml.load(stream)
        Instruction = DISASM()
        for instr in instructions:
          Buffer = struct.pack('<B', instr['seq']) 
          Target = create_string_buffer(Buffer,len(Buffer))
          Instruction.EIP = addressof(Target)
          InstrLength = Disasm(addressof(Instruction))
          assert_equal(Instruction.CompleteInstr, instr['entry'])

    def test_manyPrefixes(self):
        Buffer = b'\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\x90'
        Instruction = DISASM()
        Target = create_string_buffer(Buffer,len(Buffer))
        Instruction.EIP = addressof(Target)
        InstrLength = Disasm(addressof(Instruction))
        assert_equal(Instruction.Prefix.Number, 15)
        assert_equal(Instruction.CompleteInstr, '')


    def test_adcx(self):
        Buffer = b'\x0f\x38\xf6\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90'
        Instruction = DISASM()
        Target = create_string_buffer(Buffer,len(Buffer))
        Instruction.EIP = addressof(Target)
        InstrLength = Disasm(addressof(Instruction))
        assert_equal(Instruction.CompleteInstr, '??? ')

        Buffer = b'\x66\x0f\x38\xf6\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90'
        Instruction = DISASM()
        Target = create_string_buffer(Buffer,len(Buffer))
        Instruction.EIP = addressof(Target)
        InstrLength = Disasm(addressof(Instruction))
        assert_equal(Instruction.CompleteInstr, 'adcx dx, word ptr [eax-6F6F6F70h]')

        Buffer = b'\xf3\x0f\x38\xf6\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90'
        Instruction = DISASM()
        Target = create_string_buffer(Buffer,len(Buffer))
        Instruction.EIP = addressof(Target)
        InstrLength = Disasm(addressof(Instruction))
        assert_equal(Instruction.CompleteInstr, 'adox edx, dword ptr [eax-6F6F6F70h]')


    def test_imul(self):
        Buffer = b'\x69\x02\x83\xf6\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90'
        myDisasm = DISASM()
        myDisasm.Archi = 64
        Target = create_string_buffer(Buffer,len(Buffer))
        myDisasm.EIP = addressof(Target)
        InstrLength = Disasm(addressof(myDisasm))
        assert_equal(myDisasm.CompleteInstr, 'imul eax, dword ptr [rdx], 9090F683h')


    def test_VEX3Bytes(self):
        Buffer = b'\xc4\x82\x83\xf6\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90'
        myDisasm = DISASM()
        myDisasm.Archi = 64
        Target = create_string_buffer(Buffer,len(Buffer))
        myDisasm.EIP = addressof(Target)
        InstrLength = Disasm(addressof(myDisasm))
        assert_equal(myDisasm.Reserved_.VEX.pp, 3)
        assert_equal(myDisasm.Reserved_.VEX.L, 0)
        assert_equal(myDisasm.Reserved_.VEX.mmmmm, 2)
        assert_equal(myDisasm.Reserved_.REX.W_, 1)
        assert_equal(hex(myDisasm.Instruction.Opcode), '0xf6')
        assert_equal(~myDisasm.Reserved_.VEX.vvvv & 0b00001111, 15)
        assert_equal(myDisasm.CompleteInstr, 'mulx rdx, r15, qword ptr [r8-6F6F6F70h]')


    def test_addpd(self):
        # using REX.R to access extended xmm registers
        Buffer = b'\x44\x66\x0F\x58\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90'
        myDisasm = DISASM()
        myDisasm.Archi = 64
        Target = create_string_buffer(Buffer,len(Buffer))
        myDisasm.EIP = addressof(Target)
        InstrLength = Disasm(addressof(myDisasm))
        assert_equal(myDisasm.CompleteInstr, 'addpd xmm10, dqword ptr [rax-6F6F6F70h]')

        Buffer = b'\x66\x0F\x58\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90'
        myDisasm = DISASM()
        myDisasm.Archi = 64
        Target = create_string_buffer(Buffer,len(Buffer))
        myDisasm.EIP = addressof(Target)
        InstrLength = Disasm(addressof(myDisasm))
        assert_equal(myDisasm.CompleteInstr, 'addpd xmm2, dqword ptr [rax-6F6F6F70h]')

        Buffer = b'\xc4\x81\x81\x58\x90\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
        myDisasm = DISASM()
        myDisasm.Archi = 64
        Target = create_string_buffer(Buffer,len(Buffer))
        myDisasm.EIP = addressof(Target)
        InstrLength = Disasm(addressof(myDisasm))
        assert_equal(myDisasm.CompleteInstr, 'vaddpd xmm2, xmm15, xmmword ptr [r8+11111111h]')

        Buffer = b'\xc4\x81\x85\x58\x90\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
        myDisasm = DISASM()
        myDisasm.Archi = 64
        Target = create_string_buffer(Buffer,len(Buffer))
        myDisasm.EIP = addressof(Target)
        InstrLength = Disasm(addressof(myDisasm))
        assert_equal(myDisasm.CompleteInstr, 'vaddpd ymm2, ymm15, ymmword ptr [r8+11111111h]')

    def test_addps(self):
        # using REX.R to access extended xmm registers
        Buffer = b'\x44\x0F\x58\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90'
        myDisasm = DISASM()
        myDisasm.Archi = 64
        Target = create_string_buffer(Buffer,len(Buffer))
        myDisasm.EIP = addressof(Target)
        InstrLength = Disasm(addressof(myDisasm))
        assert_equal(myDisasm.CompleteInstr, 'addps xmm10, dqword ptr [rax-6F6F6F70h]')

        Buffer = b'\x0F\x58\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90'
        myDisasm = DISASM()
        myDisasm.Archi = 64
        Target = create_string_buffer(Buffer,len(Buffer))
        myDisasm.EIP = addressof(Target)
        InstrLength = Disasm(addressof(myDisasm))
        assert_equal(myDisasm.CompleteInstr, 'addps xmm2, dqword ptr [rax-6F6F6F70h]')

        Buffer = b'\xc4\x81\x80\x58\x90\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
        myDisasm = DISASM()
        myDisasm.Archi = 64
        Target = create_string_buffer(Buffer,len(Buffer))
        myDisasm.EIP = addressof(Target)
        InstrLength = Disasm(addressof(myDisasm))
        assert_equal(myDisasm.CompleteInstr, 'vaddps xmm2, xmm15, xmmword ptr [r8+11111111h]')

        Buffer = b'\xc4\x81\x84\x58\x90\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
        myDisasm = DISASM()
        myDisasm.Archi = 64
        Target = create_string_buffer(Buffer,len(Buffer))
        myDisasm.EIP = addressof(Target)
        InstrLength = Disasm(addressof(myDisasm))
        assert_equal(myDisasm.CompleteInstr, 'vaddps ymm2, ymm15, ymmword ptr [r8+11111111h]')

    def test_addsd(self):
        # using REX.R to access extended xmm registers
        Buffer = b'\x44\xF2\x0F\x58\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90'
        myDisasm = DISASM()
        myDisasm.Archi = 64
        Target = create_string_buffer(Buffer,len(Buffer))
        myDisasm.EIP = addressof(Target)
        InstrLength = Disasm(addressof(myDisasm))
        assert_equal(myDisasm.CompleteInstr, 'addsd xmm10, qword ptr [rax-6F6F6F70h]')

        Buffer = b'\xF2\x0F\x58\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90'
        myDisasm = DISASM()
        myDisasm.Archi = 64
        Target = create_string_buffer(Buffer,len(Buffer))
        myDisasm.EIP = addressof(Target)
        InstrLength = Disasm(addressof(myDisasm))
        assert_equal(myDisasm.CompleteInstr, 'addsd xmm2, qword ptr [rax-6F6F6F70h]')

        Buffer = b'\xc4\x81\x83\x58\x90\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
        myDisasm = DISASM()
        myDisasm.Archi = 64
        Target = create_string_buffer(Buffer,len(Buffer))
        myDisasm.EIP = addressof(Target)
        InstrLength = Disasm(addressof(myDisasm))
        assert_equal(myDisasm.CompleteInstr, 'vaddsd xmm2, xmm15, xmmword ptr [r8+11111111h]')

        Buffer = b'\xc4\x81\x87\x58\x90\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'
        myDisasm = DISASM()
        myDisasm.Archi = 64
        Target = create_string_buffer(Buffer,len(Buffer))
        myDisasm.EIP = addressof(Target)
        InstrLength = Disasm(addressof(myDisasm))
        assert_equal(myDisasm.CompleteInstr, 'vaddsd ymm2, ymm15, ymmword ptr [r8+11111111h]')

        