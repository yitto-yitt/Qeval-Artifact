# EVAL_META: task_id=8, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)
atexit.register(machine.finalize)


def rx_gate(value=None):
    theta = pq.var(0.0 if value is None else float(value), True)
    variational_circuit = pq.VariationalQuantumCircuit()
    variational_circuit.insert(pq.VariationalQuantumGate_RX(qubits[0], theta))

    circuit = variational_circuit.feed()
    program = pq.QProg()
    program.insert(circuit)
    machine.directly_run(program)

    return variational_circuit if value is None else circuit
