package main;

import java.io.IOException;

import javafx.scene.layout.VBox;

public class StreamingPage extends VBox {
	
	private static final String GET_ROOMS = "Rooms";
	
	
	public StreamingPage() {
		Communication connect;
		try {
			connect = new Communication(GET_ROOMS);
			String numberRoomsString = connect.getReturnMessage();
			
			int numRooms = Integer.getInteger(numberRoomsString);
			
			generateRooms(numRooms);
		} catch (ClassNotFoundException | IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		
	}


	private void generateRooms(int numRooms) {
		for (int i = 0; i < numRooms; i++) {
			this.getChildren().add(new StreamingPageRow("TEST",5));
		}
		
	}
}
