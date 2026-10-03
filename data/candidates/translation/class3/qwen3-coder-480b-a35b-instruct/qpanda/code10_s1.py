# EVAL_META: task_id=10, framework=qpanda, class=3
from pyqpanda import *
import numpy as np

def create_operator():
    # Define the unitary matrix
    unitary_matrix = np.array([
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [1, 0, 0, 0]
    ])
    
    # Initialize QPanda environment
    machine = init(QMachineType.CPU)
    prog = QProg()
    qubits = machine.qAlloc_many(2)
    cbits = machine.cAlloc_many(2)
    
    # Create the circuit with the unitary matrix
    circuit = QCircuit()
    circuit.insert(QOperator(unitary_matrix).to_instruction(qubits))
    
    # Decompose the circuit into single-qubit gates and CNOTs
    decomposed_circuit = circuit.decompose_to_base_qgate()
    
    # Add the decomposed circuit to the program
    prog.insert(decomposed_circuit)
    
    # Finalize and return the program
    finalize()
    return prog
