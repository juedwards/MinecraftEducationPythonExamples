import requests
import csv
import time
import matplotlib.pyplot as plt

def measure_load_time(url):
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()
    load_time = end_time - start_time
    return load_time

def record_load_time(url, load_time):
    with open('makecodeperformance.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([time.strftime('%Y-%m-%d %H:%M:%S'), url, load_time])

def plot_performance_chart():
    timestamps = []
    makecode_load_times = []
    benchmark_load_times = []

    with open('makecodeperformance.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            timestamps.append(row[0])
            if row[1] == 'https://minecraft.makecode.com/':
                makecode_load_times.append(float(row[2]))
            elif row[1] == 'https://makecode.microbit.org/':
                benchmark_load_times.append(float(row[2]))

    last_100_timestamps = timestamps[-100:]
    last_100_makecode_load_times = makecode_load_times[-100:]
    last_100_benchmark_load_times = benchmark_load_times[-100:]

    print(len(last_100_timestamps))
    print(len(last_100_makecode_load_times))
    print(len(last_100_benchmark_load_times))

    plt.plot(last_100_timestamps, last_100_makecode_load_times, label='MakeCode')
    plt.plot(last_100_timestamps, last_100_benchmark_load_times, label='Benchmark')
    plt.xlabel('Timestamp')
    plt.ylabel('Load Time (seconds)')
    plt.title('Performance Chart')
    plt.legend()
    plt.xticks(rotation=45)
    plt.show()

def main():
    makecode_url = 'https://minecraft.makecode.com/'
    benchmark_url = 'https://makecode.microbit.org/'  # Replace with your benchmark website URL
    while True:
        makecode_load_time = measure_load_time(makecode_url)
        benchmark_load_time = measure_load_time(benchmark_url)
        record_load_time(makecode_url, makecode_load_time)
        record_load_time(benchmark_url, benchmark_load_time)
        plot_performance_chart()
        time.sleep(3600)  # Sleep for 1 hour (3600 seconds)

if __name__ == '__main__':
    main()
