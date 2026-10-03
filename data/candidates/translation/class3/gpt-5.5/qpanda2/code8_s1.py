# EVAL_META: task_id=8, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)


def rx_gate(value=None):
    theta = pq.var(0.0 if value is None else float(value), value is None)
    try:
        theta.set_name("theta")
    except Exception:
        pass

    quantum_circuit = pq.VariationalQuantumCircuit()
    quantum_circuit.insert(pq.VariationalQuantumGate_RX(qubits[0], theta))
    return quantum_circuit


def _finalize_machine():
    try:
        machine.finalize()
    except Exception:
        pass


atexit.register(_finalize_machine)
