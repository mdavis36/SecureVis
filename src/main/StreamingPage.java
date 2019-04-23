package main;

import java.io.IOException;

import javafx.scene.layout.VBox;

public class StreamingPage extends VBox {
	
	private static final String GET_ROOMS = "Rooms";
	private static final String GUI = "GUI";
	
	
	public StreamingPage() {
		Communication connect;
		generateRooms(5);
		/*
		try {
			connect = new Communication(GUI + GET_ROOMS);
			String numberRoomsString = connect.getReturnMessage();
			
			int numRooms = Integer.getInteger(numberRoomsString);
			
			generateRooms(numRooms);
		} catch (ClassNotFoundException | IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} */
		
		
	}


	private void generateRooms(int numRooms) {
		for (int i = 0; i < numRooms; i++) {
			this.getChildren().add(new StreamingPageRow("TEST",5));
		}
		
	}
}
