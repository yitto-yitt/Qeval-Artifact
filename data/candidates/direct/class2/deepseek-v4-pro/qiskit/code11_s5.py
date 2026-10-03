# EVAL_META: task_id=11, framework=qiskit, class=2
from qiskit.quantum_info import Statevector

def get_statevector(circuit):
    qc = circuit.remove_final_measurements(inplace=False)
    return Statevector.from_instruction(qc)
