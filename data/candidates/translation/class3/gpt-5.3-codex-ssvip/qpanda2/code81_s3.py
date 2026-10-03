# EVAL_META: task_id=81, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)
c = machine.cAlloc_many(2)

def convert_qasm_string_to_quantum_circuit():
    qasm_string = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];"""
    prog = convert_qasm_string_to_qprog(qasm_string, machine)
    machine.finalize()
    return prog
