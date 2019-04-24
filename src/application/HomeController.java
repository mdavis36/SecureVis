package application;

import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.ResourceBundle;


import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.Slider;
import javafx.scene.layout.VBox;
import javafx.scene.media.Media;
import javafx.scene.media.MediaPlayer;
import javafx.scene.media.MediaView;
import javafx.scene.text.Text;
import javafx.util.Duration;
import main.Communication;
import main.StreamingPageRow;

public class HomeController implements Initializable {
	
	@FXML private VBox streamingPage;
	@FXML private VBox videoPage;
	@FXML private ComboBox<String> rooms;
	@FXML private ComboBox<String> dates;
	
	private static final String GET_ROOMS = "Rooms";
	private static final String GUI = "GUI";
	private static final String GET_ROOM_NAMES = "GET ROOM_NAMES";
	
	@Override
	public void initialize(URL location, ResourceBundle resources) {
		// set file path for testing
		String videoPath = new File("testFootage/test480.mp4").getAbsolutePath();
		
		
	}	
    
    @FXML // display rooms for streaming and video
    public void displayRooms() {
    	Communication connect;
    	streamingPage.getChildren().clear();
    	try {
			connect = new Communication(GUI + GET_ROOM_NAMES);
//			String[] rooms = parseRooms(connect.getReturnMessage());
//			//String numberRoomsString = connect.getReturnMessage();
//			//System.out.println(numberRoomsString);
//			//int numRooms = Integer.parseInt(numberRoomsString);
//			generateRooms(rooms);
		} catch (ClassNotFoundException | IOException e) {
			Text error = new Text("Cannot connect to master system");
			//generateRooms(4);
			streamingPage.getChildren().add(error);
		}

    }
    
    private String[] parseRooms(String returnMessage) {
		return returnMessage.split(",");
	}

	private void generateRooms(String[] rooms) {
		
		for (int i = 0; i < rooms.length; i++) {
			streamingPage.getChildren().add(new StreamingPageRow(rooms[i], 1));
		}		
	}
	

    
    @FXML // display rooms for video
    public void displayRoomsForVideo() {
    	Communication connect;
    	try {
			connect = new Communication(GUI + GET_ROOMS);			
			String[] rooms = parseRooms(connect.getReturnMessage());
			String[] test = { "1", "2", "3" };
			generateRoomsForVideo(test);
		} catch (ClassNotFoundException | IOException e) {
			Text error = new Text("Cannot connect to master system.");
			//generateRooms(4);
			streamingPage.getChildren().add(error);
		}
    }
    
    public void generateRoomsForVideo(String[] roomNames) {
		for (int i = 0; i < roomNames.length; i++) {
			rooms.getItems().add(roomNames[i]);
		}
		
		
		//rooms.setItems(listRoomNames);
	}
}
