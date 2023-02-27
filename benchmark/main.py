import zarr
import zarr.storage
from fsspec.implementations.memory import MemoryFileSystem
import numpy as np
import hashlib
import timeit


class Benchmark:
    def __init__(self):
        self._generate_data()

    def _generate_data(self):
        self.shape = (10_000, 10_000)
        # self.shape = (10, 10)
        self.dtype = np.int32

        # generate random data
        rng = np.random.default_rng(42)
        self.data_original = rng.integers(
            1, 10_000, size=self.shape, dtype=self.dtype
        )
        self.checksum_original = hashlib.sha256(
            self.data_original.data
        ).hexdigest()

    def run(self, store):
        path = "test_data"

        
        def write_to_store():
            z = zarr.zeros(self.shape, store=store, path=path, overwrite=True)
            z[:] = self.data_original
            # store.close()

        write_res = timeit.timeit(write_to_store, number=1)

        def read_from_store():
            z = zarr.open(store=store, path=path)
            data = np.array(z[:], dtype=self.dtype)
            checksum = hashlib.sha256(data.data).hexdigest()
            assert checksum == self.checksum_original

        read_res = timeit.timeit(read_from_store, number=1)

        return write_res, read_res


# def plot_matplotlib(results, title):
#     import mpld3
#     import matplotlib.pyplot as plt

#     stores = list(results.keys())
#     timings = list(results.values())

#     fig = plt.figure(figsize=(10, 5))
#     plt.bar(stores, timings, color="blue", width=0.4)
#     plt.xlabel("zarr store")
#     plt.ylabel("time taken")
#     plt.title(title)

#     # plt.show()
#     mpld3.show()


def plot_plotly(results, title):
    import plotly.express as px
    import pandas as pd

    df = pd.DataFrame.from_dict(
        {"stores": list(results.keys()), "timings": list(results.values())}
    )

    fig = px.bar(df, x="stores", y="timings", title=title)
    fig.show()


def main():
    benchmark = Benchmark()

    stores = {
        "zip": zarr.ZipStore("test_data.zip", mode="w"),
        "fsspec": zarr.storage.FSStore(
            url="", fs=MemoryFileSystem(), mode="rw"
        ),
        "dir": zarr.DirectoryStore("test_data.zarr"),
    }

    write_results = {}
    read_results = {}

    for store_name, store in stores.items():
        write_res, read_res = benchmark.run(store)
        write_results[store_name] = write_res
        read_results[store_name] = read_res

    # print read results
    print("\nread results")
    for store, time_taken in read_results.items():
        print(f"{store}\t :{time_taken}")

    # print write results
    print("\nwrite results")
    for store, time_taken in write_results.items():
        print(f"{store}:\t {time_taken}")

    # plot results
    plot_plotly(write_results, "write benchmark")
    plot_plotly(read_results, "read benchmark")


if __name__ == "__main__":
    main()
