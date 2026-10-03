# EVAL_META: task_id=8, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)


def rx_gate(value=None):
    theta = pq.var(0.0 if value is None else float(value), True)
    circuit = pq.VariationalQuantumCircuit()
    circuit.insert(pq.VariationalQuantumGate_RX(qubits[0], theta))
    return circuit if value is None else circuit.feed()


atexit.register(machine.finalize)
