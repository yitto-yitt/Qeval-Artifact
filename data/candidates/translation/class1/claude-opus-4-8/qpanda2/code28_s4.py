# EVAL_META: task_id=28, framework=qpanda2, class=1
import builtins
import pyqpanda as pq

def visualize_bell_states():
    shots = 1000

    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(2)
    cbits = machine.cAlloc_many(2)

    prog_plus = pq.QProg()
    prog_plus << pq.H(qubits[0]) \
              << pq.CNOT(qubits[0], qubits[1]) \
              << pq.measure_all(qubits, cbits)

    result_plus = machine.run_with_configuration(prog_plus, cbits, shots)
    total_plus = builtins.sum(result_plus.values())
    phi_plus = {key: value / total_plus for key, value in result_plus.items()}

    prog_minus = pq.QProg()
    prog_minus << pq.X(qubits[0]) \
               << pq.H(qubits[0]) \
               << pq.CNOT(qubits[0], qubits[1]) \
               << pq.measure_all(qubits, cbits)

    result_minus = machine.run_with_configuration(prog_minus, cbits, shots)
    total_minus = builtins.sum(result_minus.values())
    phi_minus = {key: value / total_minus for key, value in result_minus.items()}

    machine.finalize()

    return {
        "phi_plus": phi_plus,
        "phi_minus": phi_minus,
    }
