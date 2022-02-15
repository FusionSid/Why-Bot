from datetime import datetime

class Log():
    def __init__(self, path:str="./database/log.txt", timestamp:bool=True):
        self.path = path
        self.timestamp = timestamp


    def log_error(self, error):
        if self.timestamp:
            now = datetime.now()
            timern = now.strftime("%d/%m/%Y %H:%M:%S")
            log_string = f"{timern} | ERROR: {error}"
        else:
            log_string = f"ERROR: {error}"

        with open(self.path, 'a') as f:
            f.write('\n')
            f.write(log_string)

    
    def log_command_error(self, error):
        if self.timestamp:
            now = datetime.now()
            timern = now.strftime("%d/%m/%Y %H:%M:%S")
            log_string = f"{timern} | {error[0]}"
        else:
            log_string = f"{error[0]}"

        with open(self.path, 'a') as f:
            f.write(log_string)
            for i in error[1]:
                f.write(f"{timern} | {i}")


    def log_message(self, message):
        if self.timestamp:
            now = datetime.now()
            timern = now.strftime("%d/%m/%Y %H:%M:%S")
            log_string = f"{timern} | MESSAGE: {message}"
        else:
            log_string = f"ERROR: {message}"

        with open(self.path, 'a') as f:
            f.write('\n')
            f.write(log_string)


    @property
    def file(self):
        data = []
        with open(self.path, 'r') as f:
            for i in f:
                data.append(i)
        return data


    @property
    def today(self):
        data = []

        todays_date = datetime.now().strftime("%d/%m/%Y")

        with open(self.path, 'r') as f:
            for line in f:
                if todays_date in line:
                    data.append(line)
        
        return data
    

    def get_date(self, date):
        data = []

        with open(self.path, 'r') as f:
            for line in f:
                if date in line:
                    data.append(line)
        
        return data
