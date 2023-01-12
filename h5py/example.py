import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import tensorflow as tf
import zarr
import h5py

def main():
    (train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()
    assert train_images.shape == (60000, 28, 28)
    assert train_labels.shape == (60000,)

    assert test_images.shape == (10000, 28, 28)
    assert test_labels.shape == (10000,)

    # write to zipstore
    store = zarr.ZipStore("data.zip", mode="w")
    z = zarr.zeros(train_images.shape, store=store)
    z[:] = train_images
    store.close()

    if h5py.is_hdf5('data.zip'):
        h5f = h5py.File('data.zip', 'w')
        z_ds = h5f.create_dataset("z", data=z)
        z_data = z_ds[:]
        h5f.close()
    else:
        print("The file is not a valid HDF5 file.")

if __name__ == "__main__":
    main()
