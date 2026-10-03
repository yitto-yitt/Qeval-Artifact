# EVAL_META: task_id=6, framework=qpanda, class=2
import pyqpanda3 as pq
from pyqpanda3.core import *

def create_state_prep(num_qubits):
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    qubits = machine.qAlloc_many(num_qubits)
    
    prog = pq.QProg()
    
    # To prepare state |1>, we need to apply X gate to the first qubit
    # since initially all qubits are in |0> state
    prog << pq.X(qubits[0])
    
    # For multi-qubit case, if we want all qubits to be in |1> state,
    # we would apply X to all qubits, but based on the Qiskit reference
    # which uses prepare_state(1), it means preparing the computational
    # basis state corresponding to binary representation of 1
    # For n qubits, state |1> means the state where only the least significant bit is 1
    # Actually looking at Qiskit's prepare_state(1), it prepares the state |1> for single qubit
    # But for multiple qubits, prepare_state with integer prepares the corresponding basis state
    
    # In binary, the number 1 corresponds to having the least significant qubit as 1
    # So we just need to flip the first qubit (if num_qubits > 0)
    if num_qubits > 0:
        prog << pq.X(qubits[0])
    
    # Actually, let me reconsider - Qiskit's prepare_state(1) with n qubits
    # prepares the state |1> which means the computational basis state 
    # corresponding to binary 1... so for n qubits, it would be |00...01>
    # This means we only need to set the rightmost qubit (index 0 assuming LSB) to 1
    # Reset the program for clarity
    prog = pq.QProg()
    if num_qubits > 0:
        prog << pq.X(qubits[num_qubits-1])  # Set the most significant qubit position to 1 in little-endian
        
    # Actually, following the Qiskit behavior more precisely:
    # prepare_state(1) on n qubits prepares the state |1> in the computational basis
    # where 1 in binary is just 1, so we need to set up the state accordingly
    # In pyQPanda, if we want to prepare state |1> out of n qubits, 
    # it should be the state where the decimal value is 1, i.e., |0...01> in standard ordering
    # Let's use unitary operations to achieve this by flipping the appropriate qubit
    prog = pq.QProg()
    if num_qubits >= 1:
        # Flip the last qubit (in little endian, this represents |1>)
        prog << pq.X(qubits[0])
    
    return (prog, machine, qubits)
