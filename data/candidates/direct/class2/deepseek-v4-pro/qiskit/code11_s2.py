# EVAL_META: task_id=11, framework=qiskit, class=2
from qiskit.quantum_info import Statevector

def get_statevector(circuit):
    if circuit.num_clbits > 0:
        circuit = circuit.copy()
        circuit.remove_final_measurements(inplace=True)
    return Statevector.from_instruction(circuit)
