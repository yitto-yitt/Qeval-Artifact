# EVAL_META: task_id=8, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)


def rx_gate(value=None):
    theta = pq.var(0.0, True)
    quantum_circuit = pq.VariationalQuantumCircuit()
    quantum_circuit.insert(pq.VariationalQuantumGate_RX(qubits[0], theta))

    if value is None:
        return quantum_circuit

    theta.set_value(float(value))
    bound_circuit = quantum_circuit.feed()
    program = pq.QProg()
    program.insert(bound_circuit)
    machine.directly_run(program)
    return bound_circuit


atexit.register(machine.finalize)
