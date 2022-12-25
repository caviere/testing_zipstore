import net.java.dev.jzarr.ZipStore;
import net.java.dev.jzarr.Group;
import net.java.dev.jzarr.ArrayParams;
import net.java.dev.jzarr.DataType;

public class JzarrZipStoreTest {
    public static void main(String[] args) {
        
        ZipStore store = new ZipStore("data.zip", "w");

        Group root = Group.create(store);

        Group foo = root.createSubGroup("foo");
        Group bar = foo.createSubGroup("bar");

        
        ArrayParams params = new ArrayParams()
                .shape(10000, 10000).chunks(100, 100).dataType(DataType.i4);

        foo.createArray("aaa", params);
        bar.createArray("bbb", params);

        foo.fill(10000);
        bar.fill(10000);
        
        store.close();
    }
}
