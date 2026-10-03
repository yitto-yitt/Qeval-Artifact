# EVAL_META: task_id=8, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)
atexit.register(machine.finalize)


def rx_gate(value=None):
    theta = pq.var(0.0 if value is None else float(value), True)
    quantum_circuit = pq.VariationalQuantumCircuit()
    quantum_circuit.insert(pq.VariationalQuantumGate_RX(qubits[0], theta))

    bound_circuit = quantum_circuit.feed()
    program = pq.QProg()
    program.insert(bound_circuit)
    machine.directly_run(program)

    return quantum_circuit if value is None else bound_circuit
