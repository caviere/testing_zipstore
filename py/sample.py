import zarr

def main():
    store = zarr.ZipStore('data.zip', mode='w')
    root = zarr.group(store)
    foo = root.create_group("foo")
    bar = root.create_group("bar")

    foo = foo.zeros('aaa', shape=(100, 100), chunks=(10, 10), dtype='i4')
    bar = bar.zeros('bbb', shape=(100, 100), chunks=(10, 10), dtype='i4')

    foo[:] = 100
    bar[:] = 100
    store.close()

    # print (root.info)

if __name__ == "__main__":
    main()
