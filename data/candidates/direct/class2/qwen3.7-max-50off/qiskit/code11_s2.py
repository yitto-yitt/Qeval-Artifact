# EVAL_META: task_id=11, framework=qiskit, class=2
from qiskit.quantum_info import Statevector

def get_statevector(circuit):
    try:
        return Statevector(circuit)
    except Exception:
        circ = circuit.copy()
        circ.remove_final_measurements()
        return Statevector(circ)
