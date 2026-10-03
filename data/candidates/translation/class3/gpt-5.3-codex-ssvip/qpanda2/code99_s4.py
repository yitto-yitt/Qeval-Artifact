# EVAL_META: task_id=99, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(32)

def remove_unassigned_parameterized_gates(circuit):
    prog = pq.QProg()
    if isinstance(circuit, pq.QProg):
        prog << circuit
    elif isinstance(circuit, pq.QCircuit):
        prog << circuit
    machine.directly_run(prog)
    machine.finalize()
    return prog
