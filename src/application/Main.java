package application;
import java.io.IOException;

import javafx.application.Application;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.layout.BorderPane;
import javafx.stage.Stage;
import main.StreamingPage;

public class Main extends Application {
	private Stage primaryStage;
	private BorderPane homeLayout;	
		
	@Override
	public void start(Stage primaryStage) throws IOException {
		this.primaryStage = primaryStage;
		this.primaryStage.setTitle("SecureVis Security System");
		showMainApp();
	}	
	
	public static void main(String[] args) {
		launch(args);
	}
	
	// displays the main application interface
	private void showMainApp() throws IOException {
		
		// set layout to FXML file
		FXMLLoader layoutLoader = new FXMLLoader();
		layoutLoader.setLocation(Main.class.getResource("Home.fxml"));
		homeLayout = layoutLoader.load();
		
		// show the layout on the screen
		Scene mainScene = new Scene(homeLayout);
		primaryStage.setScene(mainScene);
		primaryStage.show();
	}
	

}
