package main;

import java.io.IOException;

import application.DirectoryUtil;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.scene.control.Button;
import javafx.scene.layout.HBox;
import javafx.scene.text.Text;

public class VideoPageRow extends HBox implements EventHandler<ActionEvent> {

	private Text roomName;
	private Button view;
	
	private static final String VLC = "vlc ";
	
	public VideoPageRow(String name) {
		roomName = new Text(name);
		
		view = new Button("View");
		view.setId("view");
		view.setOnAction(this);
		
		this.getChildren().addAll(roomName,view);
		this.setSpacing(10);
	}
	
	@Override
	public void handle(ActionEvent e) {
		if (e.getSource() instanceof Button) {
			Button clicked = (Button) e.getSource();
			
			if (clicked.getId().equals("view")) {
				try {
					launchVLC();
				} catch (IOException e1) {
					// TODO Auto-generated catch block
					//e1.printStackTrace();
				}
			}
		}
		
	}

	private void launchVLC() throws IOException {
		Runtime.getRuntime().exec(VLC + DirectoryUtil.VIDEO_DIRECTORY + "/" + roomName.getText());
	}

}
