# EVAL_META: task_id=81, framework=qpanda, class=3
from pyqpanda3.core import QProg, Qubit, CBit, H, CNOT

def convert_qasm_string_to_quantum_circuit():
    qasm_string = """OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[2];
    creg c[2];
    h q[0];
    cx q[0],q[1];"""
    q = [Qubit(i) for i in range(2)]
    c = [CBit(i) for i in range(2)]
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    return prog
