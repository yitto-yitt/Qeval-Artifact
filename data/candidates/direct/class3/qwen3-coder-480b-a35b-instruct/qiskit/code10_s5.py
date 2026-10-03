# EVAL_META: task_id=10, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.compiler import transpile
from qiskit.transpiler import PassManager
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager


def create_operator():
    # Create a quantum circuit with 2 qubits
    qc = QuantumCircuit(2)
    
    # The target unitary is [[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]]
    # This is equivalent to swapping the qubits followed by X gates on both qubits
    # Or equivalently: SWAP followed by X on both qubits
    # We can decompose SWAP using 3 CX gates: CX(0,1), CX(1,0), CX(0,1)
    qc.cx(0, 1)
    qc.cx(1, 0)
    qc.cx(0, 1)
    
    # Then apply X gates to both qubits to match the desired transformation
    qc.x(0)
    qc.x(1)

    # Transpile the circuit with optimization level 1
    pm = generate_preset_pass_manager(optimization_level=1)
    transpiled_circuit = pm.run(qc)
    
    return transpiled_circuit
