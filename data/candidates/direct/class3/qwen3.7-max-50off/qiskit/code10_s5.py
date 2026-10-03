# EVAL_META: task_id=10, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

def create_operator():
    qc = QuantumCircuit(2)
    qc.cx(0, 1)
    qc.cx(1, 0)
    qc.cx(0, 1)
    
    pm = generate_preset_pass_manager(optimization_level=1)
    transpiled_qc = pm.run(qc)
    
    return transpiled_qc
