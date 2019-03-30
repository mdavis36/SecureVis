import java.io.IOException;
import java.net.*;


public class Communication {
	private Socket socket;
	private static final int PORT = 65432;
	Communication() throws UnknownHostException, IOException {
		socket = new Socket(InetAddress.getLocalHost(),PORT);
	}
}
