import {zeros, ObjectStore} from "zarr"

async function main (){
    const store = new ObjectStore();

    const foo = await zeros ([100,100], {
        chunks: [10,10],
        dtype: "<i4",
        fill_value: 100,
    });

    const bar = await zeros ([100,100], {
        chunks: [10,10],
        dtype: "<i4",
        fill_value: 100,
    });

    console.log(foo.shape);
    console.log(bar.shape);
}

main()
