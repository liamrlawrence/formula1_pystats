import matplotlib.pyplot as plt
import fastf1 as ff1
import fastf1.plotting
from f1driver import F1Driver


if __name__ == "__main__":
    # Setup libs
    ff1.Cache.enable_cache("../../ff1_cache")
    ff1.plotting.setup_mpl()

    # Load session data
    session = ff1.get_session(2022, 'Japan', 'R')
    session.load()

    # Initialize Driver objects
    Driver_HAM = F1Driver('HAM', session)
    Driver_SAI = F1Driver('SAI', session)

    # Apply filters
    Driver_HAM.set_filter_lap(1)
    # Driver_SAI.set_filter_lap(1)  # SAI did not complete lap 1, so we want his full telemetry history

    # Get telemetry data
    telem_HAM = Driver_HAM.get_telemetry()
    telem_SAI = Driver_SAI.get_telemetry()

    # Initialize plot
    size = (1920, 1080)
    plt.rcParams['font.size'] = 16
    plt.rcParams['figure.figsize'] = (size[0] / 100.0, size[1] / 100.0)
    fig, ax = plt.subplots()

    # Plot data
    ax.plot(telem_HAM['Time'], telem_HAM['Speed'] / 1.609, color=ff1.plotting.team_color('Mercedes'), label="HAM")
    ax.plot(telem_SAI['Time'], telem_SAI['Speed'] / 1.609, color=ff1.plotting.team_color('Ferrari'), label="SAI")

    # Label plot
    ax.legend()
    ax.set_xlabel("Time in sec", labelpad=15)
    ax.set_ylabel("Speed in mph", labelpad=15)
    plt.suptitle(f"Car Speed Comparison \n"
                 f"{session.event['EventName']} {session.event.year} Lap 1", y=0.96)

    plt.show()
