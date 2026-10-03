# EVAL_META: task_id=10, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit
from qiskit.compiler import transpile
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.providers.fake_provider import FakeManhattan

def create_operator():
    # Define the unitary matrix
    unitary_matrix = np.array([
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [1, 0, 0, 0]
    ])
    
    # Create a quantum circuit with 2 qubits
    qc = QuantumCircuit(2)
    
    # Implement the unitary using CX gates and single-qubit gates
    # This is equivalent to applying SWAP gate
    qc.cx(0, 1)
    qc.cx(1, 0)
    qc.cx(0, 1)
    
    # Get backend for transpilation
    backend = FakeManhattan()
    
    # Generate pass manager with optimization level 1
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    
    # Transpile the circuit
    transpiled_qc = pm.run(qc)
    
    return transpiled_qc
