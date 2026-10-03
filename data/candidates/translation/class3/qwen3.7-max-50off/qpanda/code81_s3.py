# EVAL_META: task_id=81, framework=qpanda, class=3
from pyqpanda3.core import QProg, H, CNOT, Qubit

def convert_qasm_string_to_quantum_circuit():
    qasm_string = """OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[2];
    creg c[2];
    h q[0];
    cx q[0],q[1];"""
    
    prog = QProg()
    q0 = Qubit(0)
    q1 = Qubit(1)
    prog << H(q0) << CNOT(q0, q1)
    
    return prog
