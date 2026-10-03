# EVAL_META: task_id=106, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)
_composed_circuit = None


def compose_cnot_dihedral():
    global _composed_circuit
    if _composed_circuit is None:
        circ1 = pq.QCircuit()
        circ1 << pq.CNOT(qubits[0], qubits[1]) << pq.T(qubits[0])

        circ2 = pq.QCircuit()
        circ2 << pq.CNOT(qubits[0], qubits[1]) << pq.T(qubits[0])
        circ2 << pq.X(qubits[1])

        composed = pq.QCircuit()
        composed << circ1 << circ2

        program = pq.QProg()
        program << composed
        machine.directly_run(program)
        _composed_circuit = composed

    return _composed_circuit


try:
    compose_cnot_dihedral()
finally:
    machine.finalize()
