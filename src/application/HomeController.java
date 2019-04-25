package application;

import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.ResourceBundle;

import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.DatePicker;
import javafx.scene.control.Slider;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.scene.media.Media;
import javafx.scene.media.MediaPlayer;
import javafx.scene.media.MediaView;
import javafx.scene.text.Text;
import javafx.util.Duration;
import layout.StreamingPageRow;
import layout.VideoContainerLayout;

public class HomeController implements Initializable {
	
	@FXML private VBox streamingPage;
	@FXML private VBox videoPage;
	@FXML private DatePicker datePicker;

	
	private static final String GET_ROOM_COUNT = "ROOM_COUNT";
	private static final String GUI = "GUI ";
	private static final String GET_ROOM_NAMES = "GET ROOM_NAMES";
	private static final String VIDEO_DIRECTORY = "testFootage";
	
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
			String[] rooms = parseRooms(connect.getReturnMessage());
			generateRooms(rooms);
			
		} catch (ClassNotFoundException | IOException e) {
			Text error = new Text("Cannot connect to master system");
			streamingPage.getChildren().add(error);
		} 

    }
    
    private String[] parseRooms(String returnMessage) {
		return returnMessage.split(",");
	}

	private void generateRooms(String[] rooms) {
		System.out.println(rooms.length + "name " + rooms[0]);
		for (int i = 0; i < rooms.length; i++) {
			System.out.println(rooms[i]);
			if (notAnEmptyString(rooms[i])) {
			streamingPage.getChildren().add(new StreamingPageRow(rooms[i], 1));
			}
		}		
	}
	

    
    private boolean notAnEmptyString(String string) {
		// TODO Auto-generated method stub
		return !(string.equals(""));
	}

	@FXML // display rooms for video
    public void displayRoomsForVideo() {
		
		videoPage.getChildren().clear();
    	LocalDate date = datePicker.getValue();
    	
    	if (date != null) {
    		VideoContainerLayout vidContainer = new VideoContainerLayout(DirectoryUtil.parseDate(date));
    		videoPage.getChildren().add(vidContainer);
    	}
    	
    }
    	
}
