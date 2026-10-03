# EVAL_META: task_id=81, framework=qpanda, class=3
from pyqpanda3.core import *

def convert_qasm_string_to_quantum_circuit():
    qasm_string = """OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[2];
    creg c[2];
    h q[0];
    cx q[0],q[1];"""
    
    machine = init_quantum_machine(QMachineType.CPU)
    qc = machine.qAlloc_many(2)
    prog = QProg()
    
    # Parse QASM string and create the corresponding quantum program
    prog = QProg().from_string(qasm_string, machine)
    
    return prog
