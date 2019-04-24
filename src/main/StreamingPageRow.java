package main;

import java.io.IOException;
import java.net.UnknownHostException;

import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.scene.control.Button;
import javafx.scene.control.ChoiceBox;
import javafx.scene.control.TextField;
import javafx.scene.layout.HBox;
import javafx.scene.text.Text;

// create a method that queries all the room names; 
// comma delimited list of room names

// this layout is populated as rows in the streaming page view
public class StreamingPageRow extends HBox implements EventHandler<ActionEvent> {

	
	private static final String  QUERY = "GET STREAM ";
	
	private Text name;
	private int numCameras;
	
	private Button viewStream;
	private ChoiceBox cameras;
	
	public StreamingPageRow(String roomName, int numCameras) {
		name = new Text(roomName);
		this.numCameras = numCameras;
		name.setId("name");
		
		cameras = new ChoiceBox();
		cameras.setId("cameras");
		addCameraChoices();
		
		viewStream = new Button("Livestream Camera");
		viewStream.setOnAction(this);
		viewStream.setId("viewStream");
		
		this.getChildren().addAll(name,cameras,viewStream);
		
	}

	private void addCameraChoices() {
		String camera = "Camera ";
		
		for (int i = 0; i < numCameras; i++) {
			cameras.getItems().add(camera+(i+1));
		}
		
	}

	@Override
	public void handle(ActionEvent event) {
		if (event.getSource() instanceof Button) {
			Button button = (Button)event.getSource();
			
			switch(button.getId()) {
			case "viewStream":
				try {
					sendQuery();
				} catch (ClassNotFoundException | IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				break;
			default:
				System.out.println("ERROR");
			}
		}
		
	}

	
	private void sendQuery() throws UnknownHostException, ClassNotFoundException, IOException {
		Communication sendMessage = new Communication(QUERY + name.getText());
		
	}
}
