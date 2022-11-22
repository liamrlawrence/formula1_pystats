import fastf1 as ff1


class F1Driver:
    def __init__(self, name, session):
        self.name = name
        self.session = session
        self.driver_data = self.session.laps.pick_driver(self.name)
        self.filters = {}
        self.valid_filters = ['lap', 'time']

    def set_filter_lap(self, lap_number: int):
        self.filters['lap'] = lap_number

    def set_filter_time(self, start_stop_t: tuple):
        self.filters['time'] = start_stop_t

    def set_filters(self, filters: dict):
        for f in filters:
            match f:
                case 'lap':
                    self.set_filter_lap(filters[f])
                case 'time':
                    self.set_filter_time(filters[f])
                case _:
                    raise KeyError(f"Error setting filter '{f}' - does not exist. Valid filters are {self.valid_filters}")

    def reset_filters(self, filter_name: str = 'all'):
        if filter_name == 'all':
            self.filters = {}
        else:
            if filter_name not in self.valid_filters:
                raise KeyError(f"Error resetting filter '{filter_name}' - does not exist. Valid filters are {self.valid_filters}")
            self.filters.pop(filter_name, None)

    def get_telemetry(self, filters: dict = None):
        if filters:
            self.reset_filters()
            self.set_filters(filters)

        df = self.driver_data

        # Pre-telemetry filters
        if 'lap' in self.filters:
            df = df[df['LapNumber'] == self.filters['lap']].iloc[0]

        # Get telemetry data
        df = df.get_telemetry()

        # Post-telemetry filters
        if 'time' in self.filters:
            df = df[(self.filters['time'][0] <= df['Time']) & (df['Time'] <= self.filters['time'][1])]

        # Return data
        return df
