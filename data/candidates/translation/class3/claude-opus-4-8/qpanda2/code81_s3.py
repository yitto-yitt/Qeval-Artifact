# EVAL_META: task_id=81, framework=qpanda2, class=3
from pyqpanda import CPUQVM, convert_qasm_string_to_originir, convert_originir_string_to_qprog

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)
cbits = machine.cAlloc_many(2)


def convert_qasm_string_to_quantum_circuit():
    qasm_string = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];"""
    originir = convert_qasm_string_to_originir(qasm_string)
    prog = convert_originir_string_to_qprog(originir, machine)
    return prog[0]


if __name__ == "__main__":
    qc = convert_qasm_string_to_quantum_circuit()
    print(qc)
    machine.finalize()
