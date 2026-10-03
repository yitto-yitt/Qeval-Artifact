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
    circuit = QCircuit()
    for line in qasm_string.splitlines():
        line = line.strip()
        if not line or line.startswith('//') or line.startswith('OPENQASM') or line.startswith('include') or line.startswith('qreg') or line.startswith('creg'):
            continue
        if line.endswith(';'):
            line = line[:-1]
        parts = line.split()
        if parts[0] == 'h':
            qarg = parts[1]
            idx = int(qarg[qarg.find('[')+1:qarg.find(']')])
            circuit << H(q[idx])
        elif parts[0] == 'cx':
            qargs = parts[1].split(',')
            ctrl_idx = int(qargs[0][qargs[0].find('[')+1:qargs[0].find(']')])
            targ_idx = int(qargs[1][qargs[1].find('[')+1:qargs[1].find(']')])
            circuit << CNOT(q[ctrl_idx], q[targ_idx])
    return circuit

machine.finalize()
