# EVAL_META: task_id=11, framework=cirq, class=2
import cirq
import numpy as np

def get_statevector(circuit):
    qubits = sorted(circuit.all_qubits())
    return cirq.final_state_vector(circuit, qubit_order=qubits)
