# EVAL_META: task_id=11, framework=cirq, class=2
import cirq
import numpy as np

def get_statevector(circuit):
    qubits = sorted(circuit.all_qubits())
    qubit_order = list(reversed(qubits))
    simulator = cirq.Simulator(dtype=np.complex128)
    result = simulator.simulate(circuit, qubit_order=qubit_order)
    return result.final_state_vector
