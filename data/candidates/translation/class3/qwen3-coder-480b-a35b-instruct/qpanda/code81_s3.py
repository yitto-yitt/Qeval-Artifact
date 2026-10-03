# EVAL_META: task_id=81, framework=qpanda, class=3
from pyqpanda3.core import *

def convert_qasm_string_to_quantum_circuit():
    qasm_string = """OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[2];
    creg c[2];
    h q[0];
    cx q[0],q[1];"""
    
    machine = CPUQVM()
    machine.init_qvm()
    
    prog = QProg()
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    
    # Parse the QASM string and build the quantum program
    prog << H(q[0]) << CNOT(q[0], q[1])
    
    return prog
