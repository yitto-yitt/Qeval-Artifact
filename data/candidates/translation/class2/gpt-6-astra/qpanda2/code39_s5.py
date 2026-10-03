# EVAL_META: task_id=39, framework=qpanda2, class=2
import pyqpanda as pq

def create_uniform_superposition(n):
    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        qubits = machine.qAlloc_many(n)
        program = pq.QProg()
        for qubit in qubits:
            program << pq.H(qubit)
        machine.directly_run(program)
        return machine.get_qstate()
    finally:
        machine.finalize()
