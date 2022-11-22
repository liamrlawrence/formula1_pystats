import matplotlib.pyplot as plt
import fastf1 as ff1
import fastf1.plotting
from f1driver import F1Driver
from datetime import timedelta


if __name__ == "__main__":
    # Setup libs
    ff1.Cache.enable_cache("../../ff1_cache")
    ff1.plotting.setup_mpl()

    # Load session data
    session = ff1.get_session(2022, 'Monaco', 'Q')
    session.load()

    # Initialize Driver object
    Driver_PER = F1Driver('PER', session)
    Driver_PER.set_filter_time((timedelta(seconds=25), timedelta(seconds=35)))

    # Format telemetry data
    laps = [20, 22, 25]
    lap_colors = ["#4559FE", "#45B6FE", "#DAF0FF"]
    fields = ['Time', 'Speed', 'Throttle']
    data = {}
    for lap in laps:
        data[lap] = {}
        Driver_PER.set_filter_lap(lap)
        telemetry_data = Driver_PER.get_telemetry()
        for f in fields:
            data[lap][f] = telemetry_data[f]

    # Initialize plot
    size = (1920, 1080)
    plt.rcParams['font.size'] = 16
    plt.rcParams['figure.figsize'] = (size[0] / 100.0, size[1] / 100.0)
    fig, ax = plt.subplots(2)

    # Plot data
    for i, lap in enumerate(data):
        ax[0].plot(data[lap]['Time'], data[lap]['Speed'], color=lap_colors[i], label=f"Lap {lap}")
        ax[1].plot(data[lap]['Time'], data[lap]['Throttle'], color=lap_colors[i], label=f"Lap {lap}")

    # Label plot
    ax[0].legend()
    ax[0].set_ylabel("Speed in km/h", labelpad=15)
    ax[1].set_ylabel("Throttle %", labelpad=15)
    ax[1].set_xlabel("Time in sec", labelpad=15)
    plt.suptitle(f"Sergio Perez Telemetry\n"
                 f"{session.event['EventName']} {session.event.year} Qualifying", y=0.96)

    plt.show()
