# EVAL_META: task_id=5, framework=qpanda2, class=2
import pyqpanda as pq


def create_state_prep():
    global _state_prep_qvm
    if "_state_prep_qvm" not in globals():
        _state_prep_qvm = pq.CPUQVM()
        _state_prep_qvm.init_qvm()

    qubits = _state_prep_qvm.qAlloc_many(2)
    circuit = pq.QCircuit()
    circuit << pq.X(qubits[0]) << pq.I(qubits[1])

    program = pq.QProg()
    program << circuit
    _state_prep_qvm.directly_run(program)
    return circuit
