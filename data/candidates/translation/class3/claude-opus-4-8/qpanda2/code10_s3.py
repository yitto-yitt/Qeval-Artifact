# EVAL_META: task_id=10, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QProg, X

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def create_operator():
    prog = QProg()
    prog << X(qubits[0])
    prog << X(qubits[1])
    return prog

if __name__ == "__main__":
    prog = create_operator()
    result = machine.prob_run_dict(prog, qubits)
    print(result)
    machine.finalize()
