# EVAL_META: task_id=11, framework=qpanda, class=2
import pyqpanda3.core as pq
from pyqpanda3.core import *
import numpy as np

def get_statevector(circuit):
    # Convert the input circuit to a pyQPanda3 compatible form
    # Create a quantum machine
    qvm = pq.QVM()
    qvm.init_qvm()
    
    # Extract quantum and classical registers from the input circuit
    # Since we're getting a circuit object, we need to simulate it
    # and extract the state vector
    
    # Get the number of qubits from the circuit
    n_qubits = len(circuit.qubits) if hasattr(circuit, 'qubits') else 0
    
    # Create quantum and classical programs
    q = qvm.qAlloc_many(n_qubits)
    c = qvm.cAlloc_many(n_qubits)
    
    # Convert the circuit to pyQPanda3 format
    prog = pq.QProg()
    
    # Add gates from the input circuit to the program
    for instruction in circuit.data:
        gate = instruction[0]
        qubits = instruction[1]
        
        # Map qiskit gates to pyqpanda3 gates
        if gate.name == 'h':
            qubit_idx = circuit.find_bit(qubits[0])[0]
            prog.insert(pq.H(q[qubit_idx]))
        elif gate.name == 'x':
            qubit_idx = circuit.find_bit(qubits[0])[0]
            prog.insert(pq.X(q[qubit_idx]))
        elif gate.name == 'y':
            qubit_idx = circuit.find_bit(qubits[0])[0]
            prog.insert(pq.Y(q[qubit_idx]))
        elif gate.name == 'z':
            qubit_idx = circuit.find_bit(qubits[0])[0]
            prog.insert(pq.Z(q[qubit_idx]))
        elif gate.name == 's':
            qubit_idx = circuit.find_bit(qubits[0])[0]
            prog.insert(pq.S(q[qubit_idx]))
        elif gate.name == 't':
            qubit_idx = circuit.find_bit(qubits[0])[0]
            prog.insert(pq.T(q[qubit_idx]))
        elif gate.name == 'cx' or gate.name == 'cnot':
            ctrl_idx = circuit.find_bit(qubits[0])[0]
            tgt_idx = circuit.find_bit(qubits[1])[0]
            prog.insert(pq.CNOT(q[ctrl_idx], q[tgt_idx]))
        elif gate.name == 'cz':
            ctrl_idx = circuit.find_bit(qubits[0])[0]
            tgt_idx = circuit.find_bit(qubits[1])[0]
            prog.insert(pq.CZ(q[ctrl_idx], q[tgt_idx]))
        elif gate.name == 'rx':
            qubit_idx = circuit.find_bit(qubits[0])[0]
            angle = instruction[0].params[0]
            prog.insert(pq.RX(q[qubit_idx], angle))
        elif gate.name == 'ry':
            qubit_idx = circuit.find_bit(qubits[0])[0]
            angle = instruction[0].params[0]
            prog.insert(pq.RY(q[qubit_idx], angle))
        elif gate.name == 'rz':
            qubit_idx = circuit.find_bit(qubits[0])[0]
            angle = instruction[0].params[0]
            prog.insert(pq.RZ(q[qubit_idx], angle))
    
    # Get the state vector
    statevector = qvm.get_state_vector(prog)
    qvm.finalize()
    
    # Return the state vector as a complex numpy array
    return statevector
