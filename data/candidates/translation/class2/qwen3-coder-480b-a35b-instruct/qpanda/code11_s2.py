# EVAL_META: task_id=11, framework=qpanda, class=2
import pyqpanda3.core as pq
from pyqpanda3.core import *
import numpy as np

def get_statevector(circuit):
    # Convert the input circuit to pyQPanda format if needed
    # Assuming circuit is already in a compatible format or needs conversion
    
    # Create a quantum machine
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(circuit.num_qubits)
    
    # Build the program
    prog = pq.QProg()
    
    # Add gates from the input circuit
    for instruction in circuit.data:
        gate = instruction[0]
        qargs = instruction[1]
        
        if gate.name == 'h':
            prog.insert(pq.H(qubits[qargs[0].index]))
        elif gate.name == 'x':
            prog.insert(pq.X(qubits[qargs[0].index]))
        elif gate.name == 'y':
            prog.insert(pq.Y(qubits[qargs[0].index]))
        elif gate.name == 'z':
            prog.insert(pq.Z(qubits[qargs[0].index]))
        elif gate.name == 's':
            prog.insert(pq.S(qubits[qargs[0].index]))
        elif gate.name == 't':
            prog.insert(pq.T(qubits[qargs[0].index]))
        elif gate.name == 'cx' or gate.name == 'cnot':
            prog.insert(pq.CNOT(qubits[qargs[0].index], qubits[qargs[1].index]))
        elif gate.name == 'cz':
            prog.insert(pq.CZ(qubits[qargs[0].index], qubits[qargs[1].index]))
        elif gate.name == 'rx':
            prog.insert(pq.RX(qubits[qargs[0].index], gate.params[0]))
        elif gate.name == 'ry':
            prog.insert(pq.RY(qubits[qargs[0].index], gate.params[0]))
        elif gate.name == 'rz':
            prog.insert(pq.RZ(qubits[qargs[0].index], gate.params[0]))
    
    # Get the state vector
    statevector = machine.get_output_state_vector(prog)
    
    # Convert to the expected format
    # In pyQPanda, the state vector is returned as a numpy array
    # We need to wrap it appropriately to match the expected interface
    return statevector
