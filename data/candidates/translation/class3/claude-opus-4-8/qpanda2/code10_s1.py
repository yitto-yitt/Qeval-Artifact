# EVAL_META: task_id=10, framework=qpanda2, class=3
from pyqpanda import CPUQVM, X

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def create_operator():
    prog = machine.create_empty_qprog()
    prog << X(qubits[0]) << X(qubits[1])
    return prog

if __name__ == "__main__":
    program = create_operator()
    result = machine.prob_run_dict(program, qubits)
    print(result)
    machine.finalize()
