# EVAL_META: task_id=81, framework=qpanda, class=3
from pyqpanda3.core import init_cpu_qvm, convert_qasm_to_qprog, convert_qprog_to_qcircuit

def convert_qasm_string_to_quantum_circuit():
    init_cpu_qvm()
    qasm_string = """OPENQASM 2.0;
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];"""
    qprog = convert_qasm_to_qprog(qasm_string)
    return convert_qprog_to_qcircuit(qprog)
