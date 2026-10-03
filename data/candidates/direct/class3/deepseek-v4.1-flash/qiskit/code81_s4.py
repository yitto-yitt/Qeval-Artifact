# EVAL_META: task_id=81, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit import qasm2

def convert_qasm_string_to_quantum_circuit():
    qasm_str = 'OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[2];\ncreg c[2];\nh q[0];\ncx q[0],q[1];\nmeasure q[0] -> c[0];\nmeasure q[1] -> c[1];\n'
    return qasm2.loads(qasm_str)
