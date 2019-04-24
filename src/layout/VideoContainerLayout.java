package layout;
import java.util.ArrayList;

import application.DirectoryUtil;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.TitledPane;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;

public class VideoContainerLayout extends VBox {
	
	private String date;
	
	public VideoContainerLayout(String date){
		
		this.date = date;
		
		ArrayList<String> roomNames = DirectoryUtil.findRoomsByDate(date);
		
    	generateRoomPanes(roomNames);
    		
    	
	}

	private void generateRoomPanes(ArrayList<String> roomNames) {
		for (String room : roomNames) {
			 ArrayList<String> filesForRoom = DirectoryUtil.filesByDateAndName(date, room);
			 
			 VBox fileContainer = new VBox();
			 
			 for (String file: filesForRoom) {
				 fileContainer.getChildren().add(new VideoPageRow(file));
			 }
			 
			 TitledPane roomHeader = new TitledPane(room,fileContainer);
			 this.getChildren().add(roomHeader);
		}
		
	}
	
	public String getDate() {
		return date;
	}
}
