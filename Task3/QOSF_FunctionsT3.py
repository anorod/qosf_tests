# -*- coding: utf-8 -*-

# QSOF - Task 3
# by Antonio Nó Rodríguez
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
from qiskit.circuit.library.standard_gates.z import CZGate
#from qiskit.circuit._utils import _compute_control_matrix
from qiskit.qasm import pi

def qi(self, qubit, *, q=None, RGates=False):
	if RGates:
		self.rz(0, qubit)
	else:
		self.append(QIGate(), [qubit], [])

def qh(self, qubit, *, q=None, RGates=False):
	if RGates:
		self.rx(-pi/2, qubit)
		self.rz(-pi/2, qubit)
		self.rx(-pi/2, qubit)
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

def qrx(self, theta, qubit, *, q=None, RGates=False):
	if RGates:
		self.rx(theta, qubit)
	else:
		self.append(QRXGate(theta), [qubit], [])

def qry(self, theta, qubit, *, q=None, RGates=False):
	if RGates:
		if theta == 0:
			self.rz(0, qubit)
		elif theta%(2*pi) == 0:
			self.rz(0, qubit)
		else:
			self.rz(-pi/2,qubit)
			self.rx(theta,qubit)
			self.rz(pi/2,qubit)
	else:
		self.append(QRYGate(theta), [qubit], [])

def qrz(self, phi, qubit, *, q=None, RGates=False):
	if RGates:
		self.rz(phi, qubit)
	else:
		self.append(QRZGate(phi), [qubit], [])

def qcnot(self, control_qubit, target_qubit, *, label=None, ctrl_state=None, RGates=False):
	if RGates:
		self.qh(target_qubit, RGates=True)
		self.qcz(control_qubit, target_qubit, RGates=True)
		self.qh(target_qubit, RGates=True)
	else:
		self.append(QCNOTGate(ctrl_state=ctrl_state), [control_qubit, target_qubit], [])

def qcz(self, control_qubit, target_qubit, *, label=None, ctrl_state=None, RGates=False):
	if RGates:
		self.append(CZGate(label=label, ctrl_state=ctrl_state), [control_qubit, target_qubit], [])
	else:
		self.append(QCZGate(ctrl_state=ctrl_state), [control_qubit, target_qubit], [])


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
			(RXGate(-pi/2), [q[0]], []),
			(RZGate(-pi/2), [q[0]], []),
			(RXGate(-pi/2), [q[0]], [])
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

class QRXGate(Gate):
	r"""Gate that replaces the RX Gate as RX(theta)"""
	
	def __init__(self, theta, label=None):
		"""Create new QRXGate"""
		super().__init__('qrx', 1, [theta], label=label)
		
	def _define(self):
		"""
		Gate Rx(theta) to Rx(theta)
		"""
		definition = []
		q = QuantumRegister(1, 'q')
		rule = [
			(RXGate(self.params[0]), [q[0]], [])
		]
		for inst in rule:
			definition.append(inst)
		self.definition = definition

class QRYGate(Gate):
	r"""Gate that replaces the RY Gate as RY(theta)"""
	
	def __init__(self, theta, label=None):
		"""Create new QRYGate"""
		super().__init__('qry', 1, [theta], label=label)
		
	def _define(self):
		"""
		Gate Ry(theta) to Rz(-pi/2)·Rx(theta)·Rz(pi/2)
		"""
		definition = []
		q = QuantumRegister(1, 'q')
		if self.params[0] == 0:
			rule = [
				(RZGate(0), [q[0]], [])
			]
		elif self.params[0]%(2*pi)==0:
			rule = [
				(RZGate(0), [q[0]], [])
			]
		else:
			rule = [
				(RZGate(-pi/2), [q[0]], []),
				(RXGate(self.params[0]), [q[0]], []),
				(RZGate(pi/2), [q[0]], [])
			]
		for inst in rule:
			definition.append(inst)
		self.definition = definition

class QRZGate(Gate):
	r"""Gate that replaces the RZ Gate as QRZ(phi)"""
	
	def __init__(self, phi, label=None):
		"""Create new QRZGate"""
		super().__init__('qrz', 1, [phi], label=label)
		
	def _define(self):
		"""
		Gate Rz(phi) to Rz(phi)
		"""
		definition = []
		q = QuantumRegister(1, 'q')
		rule = [
			(RZGate(self.params[0]), [q[0]], [])
		]
		for inst in rule:
			definition.append(inst)
		self.definition = definition

class QCNOTGate(ControlledGate):
	r"""Gate that replaces the CNOT Gate as QH, QCZ and QH"""

	def __init__(self, label=None, ctrl_state=None):
		"""Create new CNOT gate."""
		super().__init__('qcnot', 2, [], label=label, num_ctrl_qubits=1, ctrl_state=ctrl_state)
		self.base_gate = QXGate()

	def _define(self):
		definition = []
		q = QuantumRegister(2, 'q')
		rule = [
			(QHGate(), [q[1]]),
			(QCZGate(), [q[0], q[1]], []),
			(QHGate(), [q[1]])
		]
		for inst in rule:
			definition.append(inst)
		self.definition = definition

class QCZGate(ControlledGate):
	r"""Gate that replaces the CZ Gate as QCZ"""

	def __init__(self, label=None, ctrl_state=None):
		"""Create new CZ gate."""
		super().__init__('qcz', 2, [], label=label, num_ctrl_qubits=1, ctrl_state=ctrl_state)
		self.base_gate = QZGate()

	def _define(self):
		definition = []
		q = QuantumRegister(2, 'q')
		rule = [
			(CZGate(), [q[0], q[1]], [])
		]
		for inst in rule:
			definition.append(inst)
		self.definition = definition




QuantumCircuit.qi = qi
QuantumCircuit.qh = qh
QuantumCircuit.qx = qx
QuantumCircuit.qy = qy
QuantumCircuit.qz = qz
QuantumCircuit.qrx = qrx
QuantumCircuit.qry = qry
QuantumCircuit.qrz = qrz
QuantumCircuit.qcz = qcz
QuantumCircuit.qcnot = qcnot
QuantumCircuit.qcx = qcnot