# EVAL_META: task_id=49, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)
_circuit = None


def simple_elitzur_vaidman():
    global _circuit
    if _circuit is None:
        circuit = pq.QCircuit()
        circuit << pq.H(qubits[0])
        circuit << pq.CNOT(qubits[0], qubits[1])
        circuit << pq.H(qubits[0])

        program = pq.QProg()
        program << circuit
        machine.directly_run(program)
        _circuit = circuit
    return _circuit


simple_elitzur_vaidman()
machine.finalize()
