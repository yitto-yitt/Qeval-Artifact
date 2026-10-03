# EVAL_META: task_id=2, framework=qpanda, class=2
import pyqpanda3.core as pq
from math import sqrt


def create_bell_statevector():
    # Create a quantum machine and allocate two qubits
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(2)
    
    # Create the initial |00> state
    prog = pq.QProg()
    prog.insert(pq.gate.I(qubits[0])).insert(pq.gate.I(qubits[1]))
    
    # Apply H gate to first qubit
    prog.insert(pq.gate.H(qubits[0]))
    # Apply CNOT gate with first qubit as control and second as target
    prog.insert(pq.gate.CNOT(qubits[0], qubits[1]))
    
    # Get the state vector
    statevector = machine.get_state_vector(prog)
    
    # Clean up
    machine.qFree_all(qubits)
    
    return statevector
