# EVAL_META: task_id=8, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_qubits = machine.qAlloc_many(1)
atexit.register(machine.finalize)

def rx_gate(value=None):
    if value is not None:
        circuit = pq.QCircuit()
        circuit.insert(pq.RX(_qubits[0], float(value)))
        return circuit

    theta = pq.var(0.0, True)
    circuit = pq.VariationalQuantumCircuit()
    circuit.insert(pq.VariationalQuantumGate_RX(_qubits[0], theta))
    return circuit
