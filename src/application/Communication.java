package application;
import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.EOFException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.PrintWriter;
import java.net.*;
import java.util.Scanner;

// initialize GUI, restore from state

// start server while loop
	// recieve and send data to master
	// update GUI accordingly
	// if user wants to exit settings page terminate


// change input and output streams to non java dependent things
// byte input streaam?
public class Communication {
	
	private static final int PORT = 1153;
	private static final int HEADER_SIZE = 16;
	private static final String IP = "0.0.0.0";
	
	private PrintWriter output;
	private BufferedReader input;
	//private ServerSocket server;
	private Socket connection;
	
	private InetSocketAddress endpoint; 
	
	private String message;
	
	public Communication(String messageToSend) throws UnknownHostException, IOException, ClassNotFoundException {
		// IntetAddress.getByName(null) associates server with local IP
		endpoint = new InetSocketAddress(InetAddress.getByName(IP),PORT);
		connection = new Socket();
		waitForConnection();
		setUpStreams();
		sendMessage(messageToSend);
		recieveMessage();
		close();
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
		connection.connect(endpoint);
		showMessage("Now connected to " + connection.getInetAddress().getHostName());
	}
	
	private void setUpStreams() throws IOException {
		output = new PrintWriter(connection.getOutputStream(),true);
		output.flush();
		
		input = new BufferedReader(new InputStreamReader(connection.getInputStream()));
		
		showMessage("Streams are now setup!");
	}
	
	private void showMessage(String str) {
		System.out.println(str);
	}
	
	private void sendMessage(String messageToSend) throws IOException {
		output.println(messageToSend);
		output.flush();
	}
	
	private void recieveMessage() throws ClassNotFoundException {
		try {
		 message = (String)	input.readLine();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		
	}
	
	// return message stored in this object
	public String getReturnMessage() {
		return message;
	}
	
	private void close() throws IOException {
		showMessage("closing connection");
		output.close();
		input.close();
		connection.close();
		
	}

}
