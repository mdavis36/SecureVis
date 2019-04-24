package main;
import javafx.application.*;
import javafx.event.*;
import javafx.scene.*;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.stage.*;



public class MainWindow extends Application implements EventHandler<ActionEvent> {

	// represents the entire window
	private Stage window;
	private Scene videoPage;
	
	@Override
	public void handle(ActionEvent event) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void start(Stage primaryStage) throws Exception {
		
		window = primaryStage;
		
		// generate a videoPage screen
		//VideoLayout videoLayout = new VideoLayout();
		//videoPage = new Scene(videoLayout);
		
		window.setScene(videoPage);
		window.show();
		
		
	}
	public static void main(String[] args) {
		//System.out.println("HELLO");
		launch(args);
	}

}
