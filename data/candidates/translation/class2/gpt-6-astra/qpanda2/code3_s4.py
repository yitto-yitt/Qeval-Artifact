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

    # Retain the machine that owns the program's qubits and classical bits.
    if not hasattr(create_ghz, "_machines"):
        create_ghz._machines = []
    create_ghz._machines.append(machine)

    if drawing:
        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle

        figure, axis = plt.subplots(figsize=(7, 3))
        for index in range(3):
            y = -index
            axis.plot([0, 5], [y, y], color="black", linewidth=1)
            axis.text(-0.15, y, f"q{index}", ha="right", va="center")

        axis.add_patch(Rectangle(
            (0.7, -0.2), 0.6, 0.4, facecolor="white", edgecolor="black",
            zorder=3
        ))
        axis.text(1, 0, "H", ha="center", va="center", zorder=4)

        for x, target in ((2, 1), (3, 2)):
            axis.plot([x, x], [0, -target], color="black")
            axis.plot(x, 0, "ko", markersize=6)
            axis.plot(
                x, -target, marker="o", markersize=15,
                markerfacecolor="white", markeredgecolor="black"
            )
            axis.plot(x, -target, marker="+", color="black", markersize=15)

        for index in range(3):
            y = -index
            axis.add_patch(Rectangle(
                (3.7, y - 0.2), 0.6, 0.4,
                facecolor="white", edgecolor="black", zorder=3
            ))
            axis.text(4, y, "M", ha="center", va="center", zorder=4)
            axis.text(5.1, y, f"→ c{index}", ha="left", va="center")

        axis.set_xlim(-0.6, 5.9)
        axis.set_ylim(-2.5, 0.5)
        axis.axis("off")
        figure.tight_layout()
        return ghz, figure

    return ghz
