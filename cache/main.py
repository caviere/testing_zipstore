import numpy as np
import statistics
import timeit
import hashlib
import zarr


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
    checksums = {}

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
        checksum = hashlib.sha256(random_array).hexdigest()
        checksums[k] = checksum
        second_level.array(str(k), random_array)

    return root, checksums


def main():
    # config
    max_groups_first_level = 100
    max_groups_second_level = 100
    array_shape = (10, 10)
    num_gets = 1_000
    get_path = get_path_fn(max_groups_first_level, max_groups_second_level)

    access_trace = gen_rand_access_trace(max=num_gets)
    timings = []
    keys = set(access_trace)
    print("unique keys: ", len(keys))
    print("num_gets: ", len(access_trace))
    dataset, checksums = create_dataset(
        keys, max_groups_first_level, max_groups_second_level, array_shape
    )

    for k in access_trace:
        array = dataset[get_path(k)]
        get_array = lambda: dataset[get_path(k)]
        time_taken = timeit.timeit(get_array, number=1)
        timings.append(time_taken)
        # TODO how to convert a zarr array to a numpy array
        # assert hashlib.sha256(array).hexdigest() == checksums[k]

    print("mean  : ", statistics.mean(timings))
    print("median: ", statistics.median(timings))


if __name__ == "__main__":
    main()
