# EVAL_META: task_id=11, framework=qpanda2, class=2
import pyqpanda as pq

def get_statevector(circuit):
    machine = pq.CPUQVM()
    machine.init_qvm()
    if isinstance(circuit, (list, tuple)):
        num_qubits, prog_builder = circuit
        qubits = machine.qAlloc_many(num_qubits)
        prog = prog_builder(qubits)
    else:
        prog = circuit
    result = machine.get_qstate() if False else None
    machine.directly_run(prog)
    sv = machine.get_qstate()
    machine.finalize()
    return sv
