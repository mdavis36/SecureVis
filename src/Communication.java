import java.io.IOException;
import java.net.*;
import java.util.Scanner;

// initialize GUI, restore from state

// start server while loop
	// recieve and send data to master
	// update GUI accordingly
	// if user wants to exit settings page terminate


public class Communication {
	
	private Socket socket;
	
	
	private static final int PORT = 65432;
	private static final int HEADER_SIZE = 16;
	
	Communication() throws UnknownHostException, IOException {
		socket = new Socket(InetAddress.getLocalHost(),PORT);
	}
	/*
	public String getInput() {
		try {
			Scanner in = new Scanner(socket.getInputStream());
			
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	} */
}
