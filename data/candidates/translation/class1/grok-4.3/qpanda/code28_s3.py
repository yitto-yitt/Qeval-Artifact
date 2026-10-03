# EVAL_META: task_id=28, framework=qpanda, class=1
import pyqpanda3.core as pq

def visualize_bell_states():
    qvm = pq.CPUQVM()
    qvm.initQVM()
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)
    phi_plus_circ = pq.QCircuit()
    phi_plus_circ << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1])
    phi_plus_prog = pq.QProg()
    phi_plus_prog << phi_plus_circ << pq.measure_all(qubits, cbits)
    result_phi_plus = qvm.run_with_configuration(phi_plus_prog, cbits, shots=1000)
    phi_minus_circ = pq.QCircuit()
    phi_minus_circ << pq.X(qubits[0]) << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1])
    phi_minus_prog = pq.QProg()
    phi_minus_prog << phi_minus_circ << pq.measure_all(qubits, cbits)
    result_phi_minus = qvm.run_with_configuration(phi_minus_prog, cbits, shots=1000)
    phi_plus_total = sum(result_phi_plus.values())
    phi_minus_total = sum(result_phi_minus.values())
    return {
        "phi_plus": {key: value / phi_plus_total for key, value in result_phi_plus.items()},
        "phi_minus": {key: value / phi_minus_total for key, value in result_phi_minus.items()},
    }
