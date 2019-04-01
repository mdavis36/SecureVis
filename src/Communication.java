import java.io.EOFException;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.*;
import java.util.Scanner;

// initialize GUI, restore from state

// start server while loop
	// recieve and send data to master
	// update GUI accordingly
	// if user wants to exit settings page terminate


public class Communication {
	
	private static final int PORT = 65432;
	private static final int HEADER_SIZE = 16;
	
	
	private ObjectOutputStream output;
	private ObjectInputStream input;
	private ServerSocket server;
	private Socket connection;
	
	private String message;
	
	Communication() throws UnknownHostException, IOException {
		// IntetAddress.getByName(null) associates server with local IP
		server = new ServerSocket(PORT,1,InetAddress.getByName(null));
		waitForConnection();
		setUpStreams();
		sendMessage();
		recieveMessage();
		/*
		while (true) {
			try {
				waitForConnection();
				setUpStreams();
				//sendData
				//recieveData
			} catch(EOFException eofException) {
				
			} finally {
				//close();
			}
		} */
		
	}
	
	private void waitForConnection() throws IOException {
		showMessage("Waiting for connection... ");
		connection = server.accept();
		showMessage("Now connected to " + connection.getInetAddress().getHostName());
	}
	
	private void setUpStreams() throws IOException {
		output = new ObjectOutputStream(connection.getOutputStream());
		output.flush();
		
		input = new ObjectInputStream(connection.getInputStream());
		
		showMessage("Streams are now setup!");
	}
	
	private void showMessage(String str) {
		System.out.println(str);
	}
	
	private void sendMessage() {
		try {
			output.writeObject("QUERY");
			output.flush();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	private void recieveMessage() {
		try {
		 message = (String)	input.readObject();
		} catch (ClassNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		
	}
	
	// return message stored in this object
	public String getMessage() {
		return message;
	}

}
