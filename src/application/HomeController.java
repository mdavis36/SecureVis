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
import main.Communication;
import main.StreamingPageRow;

public class HomeController implements Initializable, EventHandler<ActionEvent> {
	
	@FXML private VBox streamingPage;
	@FXML private VBox videoPage;
	
	//@FXML private ComboBox<String> dates;
	@FXML private DatePicker datePicker;
	@FXML private Button dateSearch;
	
	private ComboBox<String> rooms;
	private Button searchRooms;
	private String dateOfInterest;
	
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
//			//String numberRoomsString = connect.getReturnMessage();
//			//System.out.println(numberRoomsString);
//			//int numRooms = Integer.parseInt(numberRoomsString);
		generateRooms(rooms);
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
    	//Communication connect;
		videoPage.getChildren().clear();
    	LocalDate date = datePicker.getValue();
    	
    	if (date != null) {
    	
    	String dateFormat = parseDate(date);
    	dateOfInterest = dateFormat;
    	
    	ArrayList<String> roomsByDate = findRoomsByDate(dateFormat);
    	
    	HBox hbox = new HBox();
    	
    	rooms = new ComboBox<String>();
    	this.rooms.getItems().addAll(roomsByDate);
    	
    	searchRooms = new Button("Query");
    	searchRooms.setId("searchRooms");
    	searchRooms.setOnAction(this);
    	
    	hbox.getChildren().addAll(rooms,searchRooms);
    	videoPage.getChildren().add(hbox);
    	}
    	
    }
    
    private ArrayList<String> findRoomsByDate(String dateFormat) {
		File directory = new File(VIDEO_DIRECTORY);
		File[] filesInDir = directory.listFiles();
		ArrayList<String> rooms = new ArrayList<String>();
		for (int i = 0; i < filesInDir.length; i++) {
			if (filesInDir[i].getName().contains(dateFormat)) {
				String roomName = filesInDir[i].getName().split("_")[0];
				if (!(rooms.contains(roomName))) {
					rooms.add(roomName);
				}
			}
		}
		return rooms;
	}

	private String parseDate(LocalDate date) {
		String rtDate = "" + date.getYear(); 
		if(date.getMonthValue() < 10) {
			rtDate += "0" + date.getMonthValue();
		} else {
			rtDate += date.getMonthValue();
		}
		 rtDate	+= date.getDayOfMonth();
		 
		 return rtDate;
		
		
	}

	public void generateRoomsForVideo(String[] roomNames) {
    	this.rooms.getItems().clear();
		for (int i = 0; i < roomNames.length; i++) {
			if (notAnEmptyString(roomNames[i])) {
			rooms.getItems().add(roomNames[i]);
			}
		}
		
		
		//rooms.setItems(listRoomNames);
	}

	@Override
	public void handle(ActionEvent event) {
		if(event.getSource() instanceof Button) {
			Button clicked = (Button) event.getSource();
			
			if (clicked.getId().equals("searchRooms")) {
				ObservableList<String> list = rooms.getItems();
				
				for (String rName : list) {
					listFileNames(rName,dateOfInterest);
				}
				
			}
		}
		
	}

	private void listFileNames(String rName, String date) {
		File directory = new File(VIDEO_DIRECTORY);
		File[] filesInDir = directory.listFiles();
		ArrayList<String> rooms = new ArrayList<String>();
		for (int i = 0; i < filesInDir.length; i++) {
			if (filesInDir[i].getName().contains(date) && filesInDir[i].getName().contains(rName)) {
				Text name = new Text(filesInDir[i].getName());
				videoPage.getChildren().add(name);
			}
		}
		
	}
}
