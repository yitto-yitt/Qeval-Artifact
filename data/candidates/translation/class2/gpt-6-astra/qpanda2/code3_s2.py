# EVAL_META: task_id=3, framework=qpanda2, class=2
import pyqpanda as pq


def create_ghz(drawing=False):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(3)
    cbits = machine.cAlloc_many(3)

    ghz = pq.QProg()
    ghz << pq.H(qubits[0])
    ghz << pq.CNOT(qubits[0], qubits[1])
    ghz << pq.CNOT(qubits[0], qubits[2])
    for qubit, cbit in zip(qubits, cbits):
        ghz << pq.Measure(qubit, cbit)

    machine.run_with_configuration(ghz, cbits, 1)

    if not hasattr(create_ghz, "_machines"):
        create_ghz._machines = []
    create_ghz._machines.append(machine)

    if drawing:
        import matplotlib.pyplot as plt

        diagram = str(pq.draw_qprog(ghz, output="text"))
        lines = diagram.splitlines()
        width = max((len(line) for line in lines), default=1)
        figure = plt.figure(
            figsize=(max(6, width * 0.09), max(3, len(lines) * 0.22))
        )
        figure.text(
            0.02, 0.98, diagram,
            family="monospace",
            fontsize=10,
            va="top",
            ha="left",
        )
        return ghz, figure

    return ghz
