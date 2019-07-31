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


class TestSuite:

    def test(self):

        # 66 0F 3A 63 /r imm8
        # pcmpistri xmm1, xmm2/m128, imm8

        Buffer = '660f3a632001'.decode('hex')
        myDisasm = Disasm(Buffer)
        myDisasm.read()
        assert_equal(myDisasm.instr.Instruction.Opcode, 0xf3a63)
        assert_equal(myDisasm.instr.Instruction.Mnemonic, 'pcmpistri ')
        assert_equal(myDisasm.instr.repr, 'pcmpistri xmm4, xmmword ptr [rax], 01h')

        # VEX.128.66.0F3A 63 /r ib
        # Vpcmpistri xmm1, xmm2/m128, imm8

        myVEX = VEX('VEX.128.66.0F3A.')
        Buffer = '{}631033'.format(myVEX.c4()).decode('hex')
        myDisasm = Disasm(Buffer)
        myDisasm.read()
        assert_equal(myDisasm.instr.Instruction.Opcode, 0x63)
        assert_equal(myDisasm.instr.Instruction.Mnemonic, 'vpcmpistri ')
        assert_equal(myDisasm.instr.repr, 'vpcmpistri xmm10, xmmword ptr [r8], 33h')
