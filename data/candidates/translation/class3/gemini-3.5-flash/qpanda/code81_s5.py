# EVAL_META: task_id=81, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, convert_qasm_string_to_qprog

def convert_qasm_string_to_quantum_circuit():
    machine = CPUQVM()
    machine.init_qvm()
    qasm_string = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];"""
    prog = convert_qasm_string_to_qprog(qasm_string, machine)
    return prog
