# EVAL_META: task_id=81, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)
cbits = machine.cAlloc_many(2)

def convert_qasm_string_to_quantum_circuit():
    qasm_string = 'OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[2];\ncreg c[2];\nh q[0];\ncx q[0],q[1];'
    prog = pq.transform_qasm_to_qprog(qasm_string, machine)
    return prog

machine.finalize()
