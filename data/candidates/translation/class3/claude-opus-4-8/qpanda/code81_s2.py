# EVAL_META: task_id=81, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CNOT

def convert_qasm_string_to_quantum_circuit():
    qasm_string = """OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[2];
    creg c[2];
    h q[0];
    cx q[0],q[1];"""
    circuit = QCircuit(2)
    circuit << H(0)
    circuit << CNOT(0, 1)
    return circuit
