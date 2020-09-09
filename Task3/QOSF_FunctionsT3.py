# -*- coding: utf-8 -*-

# QSOF - Task 3
#
# Please write a simple compiler – program, which translates one quantum circuit into another, 
#  using a restricted set of gates.
# You need to consider just the basic gates for the input circuit, such as 
#  (I, H, X, Y, Z, RX, RY, RZ, CNOT, CZ).
# The output circuit should consist only from the following gates: 
#  RX, RZ, CZ. In other words, each gate in the original circuit must be replaced by an 
#  equivalent combination of gates coming from the restricted set (RX, RZ, CZ) only.
# For example, a Hadamard gate after compilation looks like this:
#  RX(pi/2)
#  RZ(pi/2)
#
# Analyze what’s the overhead of the compiled program compared to the original one and propose 
#  how to improve it. What we mean by overhead is the following: by replacing all the initial 
#  gates with the restricted set of gates given in the problem, you will see that the resulting 
#  circuit is much more involved than the original one. This is what we called the overhead, and 
#  you may think how to treat this problem, i.e. you could try to simplify as much as possible 
#  the resulting circuit.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

""" H, X, Y, Z, RX, RY, RZ, CNOT, CZ """


import numpy as np
#from math import ceil
from qiskit.circuit.controlledgate import ControlledGate
from qiskit.circuit.gate import Gate
from qiskit.circuit.quantumregister import QuantumRegister
from qiskit.circuit import QuantumCircuit, Qubit
from qiskit.quantum_info import OneQubitEulerDecomposer
from qiskit.circuit.library.standard_gates.rx import RXGate
from qiskit.circuit.library.standard_gates.rz import RZGate
#from qiskit.circuit.library.standard_gates.cz import CZGate
#from qiskit.circuit._utils import _compute_control_matrix
from qiskit.qasm import pi

def qi(self, qubit, *, q=None, RGates=False):
	if RGates:
		self.rz(0, qubit)
	else:
		self.append(QIGate(), [qubit], [])

def qh(self, qubit, *, q=None, RGates=False):
	if RGates:
		self.rx(pi/2, qubit)
		self.rz(pi/2, qubit)
	else:
		self.append(QHGate(), [qubit], [])

def qx(self, qubit, *, q=None, RGates=False):
	if RGates:
		self.rz(-pi, qubit)
		self.rx(pi, qubit)
		self.rz(pi, qubit)
	else:
		self.append(QXGate(), [qubit], [])

def qy(self, qubit, *, q=None, RGates=False):
	if RGates:
		self.rz(-pi/2, qubit)
		self.rx(pi, qubit)
		self.rz(pi/2, qubit)
	else:
		self.append(QYGate(), [qubit], [])

def qz(self, qubit, *, q=None, RGates=False):
	if RGates:
		self.rz(pi, qubit)
	else:
		self.append(QZGate(), [qubit], [])

class QIGate(Gate):
	r"""Gate that replaces the I Gate as Rz(0)"""
	
	def __init__(self, label=None):
		"""Create new QIGate"""
		super().__init__('QI', 1, [], label=label)
		
	def _define(self):
		"""
		Gate I to Rz(0)
		"""
		definition = []
		q = QuantumRegister(1, 'q')
		rule = [
			(RZGate(0), [q[0]], [])
		]
		for inst in rule:
			definition.append(inst)
		self.definition = definition

class QHGate(Gate):
	r"""Gate that replaces the H Gate as Rx(pi/2) followed by Rz(pi/2)"""
	
	def __init__(self, label=None):
		"""Create new QHGate"""
		super().__init__('QH', 1, [], label=label)
		
	def _define(self):
		"""
		Gate H to Rx(pi/2)·Rz(pi/2)
		"""
		definition = []
		q = QuantumRegister(1, 'q')
		rule = [
			(RXGate(pi/2), [q[0]], []),
			(RZGate(pi/2), [q[0]], [])
		]
		for inst in rule:
			definition.append(inst)
		self.definition = definition


class QXGate(Gate):
	r"""Gate that replaces the X Gate as Rz(-pi)·Rx(pi)·Rz(pi)"""
	
	def __init__(self, label=None):
		"""Create new QXGate"""
		super().__init__('QX', 1, [], label=label)
		
	def _define(self):
		"""
		Gate X to Rz(-pi)·Rx(pi)·Rz(pi)
		"""
		definition = []
		q = QuantumRegister(1, 'q')
		rule = [
			(RZGate(-pi), [q[0]], []),
			(RXGate(pi), [q[0]], []),
			(RZGate(pi), [q[0]], [])
		]
		for inst in rule:
			definition.append(inst)
		self.definition = definition
		
class QYGate(Gate):
	r"""Gate that replaces the Y Gate as Rz(-pi/2)·Rx(pi)·Rz(pi/2)"""
	
	def __init__(self, label=None):
		"""Create new QXGate"""
		super().__init__('QY', 1, [], label=label)
		
	def _define(self):
		"""
		Gate Y to Rz(-pi/2)·Rx(pi)·Rz(pi/2)
		"""
		definition = []
		q = QuantumRegister(1, 'q')
		rule = [
			(RZGate(-pi/2), [q[0]], []),
			(RXGate(pi), [q[0]], []),
			(RZGate(pi/2), [q[0]], [])
		]
		for inst in rule:
			definition.append(inst)
		self.definition = definition
		

class QZGate(Gate):
	r"""Gate that replaces the Z Gate as Rz(pi)"""
	
	def __init__(self, label=None):
		"""Create new QZGate"""
		super().__init__('QZ', 1, [], label=label)
		
	def _define(self):
		"""
		Gate Z to Rz(pi)
		"""
		definition = []
		q = QuantumRegister(1, 'q')
		rule = [
			(RZGate(pi), [q[0]], [])
		]
		for inst in rule:
			definition.append(inst)
		self.definition = definition
		
QuantumCircuit.qi = qi
QuantumCircuit.qh = qh
QuantumCircuit.qx = qx
QuantumCircuit.qy = qy
QuantumCircuit.qz = qz