import zarr.storage
import numpy as np
import statistics
import timeit
import hashlib
import zarr
import os


def gen_rand_access_trace(max=None):
    np.random.seed(42)
    ns = np.random.zipf(1.5, max)
    # ns = np.random.zipf(5, max)
    return ns


def get_path_fn(max_groups_first_level, max_groups_second_level):
    def get(k):
        first_level = str(k % max_groups_first_level)
        second_level = str(k % max_groups_second_level)
        return f"/{first_level}/{second_level}/{k}"

    return get


def create_dataset(
    keys, max_groups_first_level, max_groups_second_level, array_shape
):
    dtype = np.int32

    rng = np.random.default_rng(42)

    root = zarr.group()
    for k in keys:
        # access first level
        first_level_key = str(k % max_groups_first_level)
        try:
            first_level = root[f"/{first_level_key}"]
        except KeyError:
            first_level = root.create_group(f"/{first_level_key}")

        # access second level
        second_level_key = str(k % max_groups_second_level)
        try:
            second_level = first_level[f"{second_level_key}"]
        except KeyError:
            second_level = first_level.create_group(f"{second_level_key}")

        random_array = rng.integers(1, 10_000, size=array_shape, dtype=dtype)
        second_level.array(str(k), random_array)

    return root


def benchmark_store(store, access_trace, get_path):
    timings = []
    for k in access_trace:
        get_array = lambda: store[get_path(k)]
        time_taken = timeit.timeit(get_array, number=1)
        timings.append(time_taken)
    return timings


def main():
    # config
    max_groups_first_level = 100
    max_groups_second_level = 100
    array_shape = (1000, 1000)
    num_gets = 100_000
    get_path = get_path_fn(max_groups_first_level, max_groups_second_level)

    access_trace = gen_rand_access_trace(max=num_gets)
    keys = set(access_trace)
    # assume cache can hold 20% of unique keys
    cache_size = int(len(keys) * 0.2)

    print("cache_size: ", cache_size)
    print("unique keys: ", len(keys))
    print("num_gets: ", len(access_trace))

    # create dataset
    in_memory_dataset = create_dataset(
        keys, max_groups_first_level, max_groups_second_level, array_shape
    )

    # copy dataset to zipstore which will serve as the 'further' store
    dataset_path = "data.zip"
    try:
        os.remove(dataset_path)
    except FileNotFoundError:
        pass

    with zarr.ZipStore(dataset_path, mode="w") as store:
        dataset = zarr.group(store=store)

        zarr.convenience.copy_store(
            in_memory_dataset.store, store, if_exists="skip"
        )

    print()

    # benchmark store (without caching)
    with zarr.ZipStore(dataset_path, mode="r") as store:
        dataset = zarr.group(store=store)
        timings = benchmark_store(in_memory_dataset, access_trace, get_path)

        print("[zip] mean  : ", statistics.mean(timings))
        print("[zip] median: ", statistics.median(timings))

    print()

    # benchmark store (with LRU caching)
    with zarr.ZipStore(dataset_path, mode="r") as store:
        lru_store = zarr.LRUStoreCache(store=store, max_size=cache_size)
        dataset = zarr.group(store=lru_store)
        timings = benchmark_store(in_memory_dataset, access_trace, get_path)

        print("[lru] mean  : ", statistics.mean(timings))
        print("[lru] median: ", statistics.median(timings))

    print()

    # benchmark in-memory store
    timings = benchmark_store(in_memory_dataset, access_trace, get_path)
    print("[mem] mean  : ", statistics.mean(timings))
    print("[mem] median: ", statistics.median(timings))


if __name__ == "__main__":
    main()
