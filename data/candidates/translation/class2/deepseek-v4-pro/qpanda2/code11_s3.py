# EVAL_META: task_id=11, framework=qpanda2, class=2
import pyqpanda as pq

def get_statevector(circuit):
    try:
        pq.init_quantum_machine(pq.QMachineType.CPU)
    except Exception:
        pass

    prog = pq.QProg()
    prog << circuit

    if hasattr(circuit, 'get_used_qubits'):
        qubits = circuit.get_used_qubits()
    else:
        qubits = prog.get_used_qubits()

    return pq.get_state(prog, qubits)
