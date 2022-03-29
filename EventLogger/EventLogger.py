from typing import List

import logger
import dataclasses
import datetime

@dataclasses.dataclass()
class simulation_event:
    time : datetime.datetime
    func_called : str
    params: str
    event_type: str

    #todo: get dataclass from file


class eventlogger:
    """
    Keeps track of events that happen
    """
    def __init__(self, loggingfile = "log_logging_file.log", start_time = datetime.datetime.now()):
        self.version = 1.0
        self.starting_time = start_time

        self.save_location = loggingfile
        self.tracked_events : List[simulation_event] = []
        self.logfile = open(f".//logs//{self.save_location}_{self.starting_time.strftime('%d_%b_%Y_%H_%M_S')}.log", 'w')
        self.logfile.write(f"Start EventLogger {self.starting_time}\n")
        self.logfile.write(f"Start EventLogger {self.version}\n")
        print(f"Event Logger started at {self.starting_time}\nSaving to .\\{self.save_location}")



    def add_event(self, params) -> None:
        """
        Adds a new detected event to the event logger -> params [event_func, event_type, function_parameters]
        :rtype: object
        :param params [event_func, event_type, function_parameters]:
        :return None:
        """
        if callable(params[0]):
            event_func_called = params[0].__name__
        else:
            event_func_called = params[0]

        new_event = simulation_event(time=datetime.datetime.now(),
                                     func_called= event_func_called,
                                     event_type=params[1],
                                     params= params[1:]
                                     )
        self.tracked_events.append(new_event)
        self.logfile.write(f"{self.tracked_events[-1]}\n")

    def update_log_file(self):
        print(f"Writing event log file to {self.save_location}")

    def open_new_log(self):
        self.logfile = open(f".//logs//{self.save_location}_{datetime.datetime.now().strftime('%d_%b_%Y_%H_%M_S')}.log", 'w')

    def finish_log(self):
        self.logfile.close()




if __name__ == '__main__':
    main_event_logger = eventlogger()
    main_event_logger.add_event(['ship_attack','Ship Attack','Ship1','Ship2'])
    print(f"{main_event_logger.tracked_events}")
    main_event_logger.update_log_file()