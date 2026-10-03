# EVAL_META: task_id=10, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

def create_operator():
    # Build the circuit that implements the unitary [[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0]]
    # using only single-qubit gates and CX gates.
    qc = QuantumCircuit(2)
    qc.x(0)
    qc.x(1)
    qc.cx(0, 1)
    qc.cx(1, 0)
    qc.cx(0, 1)
    qc.x(0)
    qc.x(1)

    # Transpile using a pass manager with optimization level 1,
    # basis gates restricted to single-qubit U and CX.
    pm = generate_preset_pass_manager(
        optimization_level=1,
        basis_gates=['u', 'cx']
    )
    transpiled_qc = pm.run(qc)
    return transpiled_qc
