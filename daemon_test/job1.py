import datetime

current_time = datetime.datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

with open("output.txt", "a") as file:
    file.write("Exec test job_1 at: " + formatted_time + "\n")