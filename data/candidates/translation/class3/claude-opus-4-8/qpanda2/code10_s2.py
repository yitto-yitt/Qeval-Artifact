# EVAL_META: task_id=10, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, QProg, X

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def create_operator():
    circ = QCircuit()
    circ << X(qubits[0])
    circ << X(qubits[1])
    prog = QProg()
    prog << circ
    return prog


if __name__ == "__main__":
    program = create_operator()
    result = machine.prob_run_dict(program, qubits)
    print(result)
    machine.finalize()
